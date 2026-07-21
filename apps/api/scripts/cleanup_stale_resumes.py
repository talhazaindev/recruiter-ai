"""One-off cleanup: remove resume records whose stored file is missing.

A resume is "stale" if its ``source_ref.storage_key`` has no bytes in the
current storage backend (GridFS). These were uploaded to the old local MinIO
whose data is gone, so their file preview can never succeed and the unique
sha256 index blocks re-upload. This deletes the stale resume documents along
with the match_results and candidate documents derived from them, so the CVs
can be re-uploaded cleanly.

Run inside the api container:
    docker exec -i recruiter-ai-api-1 python - < apps/api/scripts/cleanup_stale_resumes.py
"""

from __future__ import annotations

import asyncio

from bson import ObjectId

from app.db import connect_db, get_db
from app.services.storage import download_bytes


def _as_object_id(value: object) -> object:
    """Best-effort convert a candidate id string to ObjectId."""
    try:
        return ObjectId(value)  # type: ignore[arg-type]
    except Exception:
        return value


async def main() -> None:
    """Find stale resumes and cascade-delete their derived records."""
    await connect_db()
    db = get_db()

    stale: list[dict] = []
    async for r in db.resumes.find({}):
        ref = r.get("source_ref") or {}
        key = ref.get("storage_key")
        ok = False
        if key:
            try:
                download_bytes(key)
                ok = True
            except Exception:
                ok = False
        if not ok:
            stale.append(r)

    total = await db.resumes.count_documents({})
    print(f"Total resumes: {total}")
    print(f"Stale resumes: {len(stale)}")

    if not stale:
        print("Nothing to clean up.")
        return

    resume_ids = [r["_id"] for r in stale]
    resume_id_strs = [str(rid) for rid in resume_ids]
    candidate_ids = [r.get("candidate_id") for r in stale if r.get("candidate_id")]
    candidate_oids = [_as_object_id(c) for c in candidate_ids]

    for r in stale:
        ref = r.get("source_ref") or {}
        print(
            f"  - resume {r['_id']} file={ref.get('original_filename')} "
            f"job={r.get('job_id')} candidate={r.get('candidate_id')}"
        )

    mr_by_candidate = await db.match_results.delete_many(
        {"candidate_id": {"$in": candidate_ids}}
    )
    mr_by_resume = await db.match_results.delete_many(
        {"resume_id": {"$in": resume_id_strs}}
    )
    cand_deleted = await db.candidates.delete_many({"_id": {"$in": candidate_oids}})
    res_deleted = await db.resumes.delete_many({"_id": {"$in": resume_ids}})

    print(
        f"Deleted: resumes={res_deleted.deleted_count} "
        f"candidates={cand_deleted.deleted_count} "
        f"match_results={mr_by_candidate.deleted_count + mr_by_resume.deleted_count}"
    )
    print("Done. Re-upload the CVs to repopulate them in GridFS.")


if __name__ == "__main__":
    asyncio.run(main())
