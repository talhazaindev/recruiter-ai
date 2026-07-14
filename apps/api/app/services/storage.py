"""S3-compatible object storage (MinIO) for CV files."""

from __future__ import annotations

import io
from functools import lru_cache

import boto3
from botocore.client import Config

from app.config import get_settings


@lru_cache
def get_s3_client():
    """Build a boto3 S3 client pointed at MinIO / S3."""
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
        use_ssl=settings.s3_use_ssl,
        config=Config(signature_version="s3v4"),
    )


def ensure_bucket() -> None:
    """Create the resume bucket if missing."""
    settings = get_settings()
    client = get_s3_client()
    try:
        client.head_bucket(Bucket=settings.s3_bucket)
    except Exception:
        client.create_bucket(Bucket=settings.s3_bucket)


def upload_bytes(key: str, data: bytes, content_type: str) -> str:
    """Upload raw bytes and return the storage key."""
    settings = get_settings()
    client = get_s3_client()
    client.upload_fileobj(
        io.BytesIO(data),
        settings.s3_bucket,
        key,
        ExtraArgs={"ContentType": content_type},
    )
    return key


def download_bytes(key: str) -> bytes:
    """Download object bytes by key."""
    settings = get_settings()
    client = get_s3_client()
    buf = io.BytesIO()
    client.download_fileobj(settings.s3_bucket, key, buf)
    return buf.getvalue()
