"""Authentication routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import create_access_token, get_current_user, verify_password
from app.config import get_settings
from app.db import get_db
from app.models.schemas import LoginRequest, TokenResponse, UserPublic

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest) -> TokenResponse:
    """Exchange email/password for a JWT."""
    db = get_db()
    user = await db.users.find_one({"email": body.email.lower()})
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(
        {
            "sub": str(user["_id"]),
            "org_id": user.get("org_id", get_settings().default_org_id),
            "role": user.get("role", "hr"),
        }
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(user: UserPublic = Depends(get_current_user)) -> UserPublic:
    """Return the current authenticated user."""
    return user
