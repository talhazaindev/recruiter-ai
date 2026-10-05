"""JWT authentication helpers and FastAPI dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import Settings, get_settings
from app.db import get_db
from app.models.schemas import UserPublic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain, hashed)


def create_access_token(
    data: dict[str, Any],
    settings: Settings | None = None,
    expires_minutes: int | None = None,
) -> str:
    """Create a signed JWT access token."""
    settings = settings or get_settings()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    settings: Settings = Depends(get_settings),
) -> UserPublic:
    """Resolve the authenticated user from the Bearer token."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    db = get_db()
    doc = await db.users.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return UserPublic(
        id=str(doc["_id"]),
        email=doc["email"],
        role=doc.get("role", "hr"),
        org_id=doc.get("org_id", settings.default_org_id),
    )


async def seed_admin_user() -> None:
    """Ensure a default admin user exists for single-org bootstrap."""
    settings = get_settings()
    db = get_db()
    existing = await db.users.find_one({"email": settings.admin_email})
    if existing:
        return
    now = datetime.now(timezone.utc)
    await db.users.insert_one(
        {
            "email": settings.admin_email,
            "password_hash": hash_password(settings.admin_password),
            "role": "admin",
            "org_id": settings.default_org_id,
            "created_at": now,
            "updated_at": now,
        }
    )
