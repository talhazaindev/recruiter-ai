"""One-off: reparse a stored resume with the local adapter."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "api"))
sys.path.insert(0, str(ROOT))

from motor.motor_asyncio import AsyncIOMotorClient

from app.services.parser_adapter import parse_resume_bytes
from app.services.storage import download_bytes


async def main() -> None:
    db = AsyncIOMotorClient("mongodb://localhost:27017")["recruiter_ai"]
    r = await db.resumes.find_one(sort=[("created_at", -1)])
    assert r, "no resumes"
    ref = r["source_ref"]
    print("file", ref.get("original_filename"))
    data = download_bytes(ref["storage_key"])
    print("bytes", len(data))
    out = parse_resume_bytes(data, ref["original_filename"])
    print("status", out.status, "conf", out.confidence, "parser", out.provenance)
    print("name", out.candidate.name)
    print("emails", out.candidate.emails)
    print("skills", (out.resume.skills if out.resume else [])[:20])
    print("experience", len(out.resume.experience) if out.resume else 0)
    if out.resume and out.resume.experience:
        e = out.resume.experience[0]
        print("exp0 company=", e.company[:100])
        print("exp0 desc=", e.description[:200])
    print("education", len(out.resume.education) if out.resume else 0)
    if out.resume and out.resume.education:
        print("edu0=", out.resume.education[0].degree[:200])
    print("warnings", out.warnings)


if __name__ == "__main__":
    asyncio.run(main())
