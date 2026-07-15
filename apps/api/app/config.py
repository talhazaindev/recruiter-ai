"""Application configuration from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    secret_key: str = "change-me-to-a-long-random-string"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    default_org_id: str = "default"

    admin_email: str = "admin@recruiter.ai"
    admin_password: str = "admin123456"

    # Atlas only — no local MongoDB.
    mongodb_uri: str = ""
    mongodb_db: str = "RecruiterAI"

    redis_url: str = "redis://localhost:6379/0"

    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "resumes"
    s3_region: str = "us-east-1"
    s3_use_ssl: bool = False

    parse_confidence_review_threshold: float = 0.55
    groq_api_key: str = ""
    groq_model: str = "qwen/qwen3-32b"

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/v1/integrations/drive/callback"

    access_token_expire_minutes: int = 60 * 24

    @field_validator("mongodb_uri")
    @classmethod
    def require_atlas_uri(cls, value: str) -> str:
        """Reject local MongoDB; require an Atlas mongodb+srv URI."""
        uri = (value or "").strip()
        if not uri:
            raise ValueError(
                "MONGODB_URI is required. Use Atlas: "
                "mongodb+srv://...@recruit....mongodb.net/?appName=recruit"
            )
        lowered = uri.lower()
        if not lowered.startswith("mongodb+srv://"):
            raise ValueError(
                "MONGODB_URI must be an Atlas mongodb+srv:// URI. Local MongoDB is not allowed."
            )
        if "localhost" in lowered or "127.0.0.1" in lowered or "@mongo:" in lowered or "//mongo:" in lowered:
            raise ValueError("Local MongoDB hosts are not allowed. Use MongoDB Atlas only.")
        return uri

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()
