"""Seed admin user (also runs on API startup)."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.auth import seed_admin_user  # noqa: E402
from app.db import close_db, connect_db  # noqa: E402


async def main() -> None:
    """Connect, seed admin, disconnect."""
    await connect_db()
    await seed_admin_user()
    print("Admin user ensured.")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
