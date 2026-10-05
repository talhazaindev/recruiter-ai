"""FastAPI application entrypoint."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import seed_admin_user
from app.config import get_settings
from app.db import close_db, connect_db
from app.routes import auth, calls, drive, health, ingest, jobs, reference, results
from app.services.storage import ensure_bucket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recruiter-api")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Startup / shutdown hooks."""
    settings = get_settings()
    await connect_db()
    try:
        ensure_bucket()
    except Exception as exc:
        logger.warning("Object storage bucket init deferred: %s", exc)
    await seed_admin_user()
    logger.info("API ready (env=%s)", settings.app_env)
    yield
    await close_db()


def create_app() -> FastAPI:
    """Build the FastAPI application."""
    settings = get_settings()
    app = FastAPI(
        title="Recruiter AI API",
        version="0.1.0",
        description="JD → ingest → parse → hybrid match → shortlist / review",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(jobs.router)
    app.include_router(ingest.router)
    app.include_router(results.router)
    app.include_router(drive.router)
    app.include_router(calls.router)
    app.include_router(reference.router)
    return app


app = create_app()
