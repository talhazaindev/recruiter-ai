# Recruiter AI

Production-oriented ATS shell: **JD → CV ingest (upload / Google Drive) → parse → hybrid match → dashboard → shortlist / review**, with stubs for future AI voice screening.

## Stack

| Layer | Tech |
|---|---|
| Web | React + Vite + TypeScript + Tailwind + TanStack Query + Framer Motion |
| API | FastAPI + Motor (MongoDB) + JWT auth |
| Queue | Redis lists (`parse` / `match` / `ingest` workers) |
| Files | MinIO (S3-compatible) |
| Matcher | `services/matcher` stub (swap for teammate pipeline) |
| Parser | Stub adapter (`PARSER_MODE=stub`) or local package (`PARSER_MODE=local`) |

## Quick start (Docker — whole stack)

One command from the repo root (API, web, workers, Mongo, Redis, MinIO):

```bash
cp .env.example .env   # first time only; optional overrides / secrets
docker compose up --build
```

| Service | URL |
|---|---|
| Web | http://localhost:5173 |
| API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |
| MinIO console | http://localhost:9001 |

Sign in: `admin@recruiter.ai` / `admin123456`

Detached: `docker compose up --build -d` · Stop: `docker compose down`

## Quick start (local processes)

### 1. Infrastructure only

```bash
docker compose up mongo redis minio -d
```

Defaults: Mongo `localhost:27017`, Redis `localhost:6379`, MinIO `localhost:9000` (minioadmin / minioadmin).

### 2. Environment

```bash
cp .env.example .env
```

For local (non-Docker) API, set in `.env`:

```
MONGODB_URI=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0
S3_ENDPOINT=http://localhost:9000
```

### 3. API

```bash
cd apps/api
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="../../;$PWD"   # PowerShell — repo root + api on path
uvicorn app.main:app --reload --port 8000
```

Seed admin (also auto-runs on API startup): `admin@recruiter.ai` / `admin123456`

### 4. Workers (recommended)

In separate terminals (from repo root, with `apps/api` deps installed):

```bash
$env:PYTHONPATH="$PWD\apps\api;$PWD"
python workers/parse_worker.py
python workers/match_worker.py
python workers/ingest_worker.py
```

If Redis is down, upload ingest falls back to **inline** parse+match inside the API so demos still work.

### 5. Web

```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:5173 — sign in with the seed admin.

## Day-to-day flow

1. Create a job → edit JD (must-have skills drive hard filters).
2. Ingest → upload PDFs/DOCX and/or paste a Drive folder URL.
3. Watch pipeline progress (Queued → Parsing → Matching → Done).
4. Results → sort/filter → shortlist.
5. Shortlist → full contacts; Review → approve/reject low-confidence parses.
6. **AI Call** buttons create `screening_calls` stub records (voice agent later).

## Google Drive

1. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` in `.env`.
2. From Ingest, click **Connect Drive** (OAuth).
3. Paste a folder URL → ingest worker downloads PDF/DOCX into the same pipeline.

Without OAuth credentials, Drive ingest fails with a clear batch error; uploads still work.

## Plugging in teammate matcher

Replace logic in [`services/matcher/`](services/matcher/) keeping:

```python
def match_jd_resume(jd, resume) -> MatchOutput
```

Return shape: `hard_filters`, `score`, `rank_signals`, `explanation`, `matcher_version`.

## Scaling

- Scale **parse workers** first for large Drive folders.
- Keep separate Redis queues so matching is not starved by parse.
- Mongo indexes are created on API/worker startup (`org_id`, job score, shortlist, review).
- Add `org_id` sharding later for multi-tenant SaaS; v1 uses `DEFAULT_ORG_ID=default`.

## Docling models (Docker)

Multi-column resumes use Docling. Model weights are **baked into the image at build time** (`infra/Dockerfile.api`), not downloaded on first parse or ingest.

| Setting | Default | Purpose |
|---|---|---|
| `DOCLING_ARTIFACTS_PATH` | `/opt/docling/models` | Pre-downloaded model directory inside the image |
| `DOCLING_DO_OCR` | `false` | OCR off — resumes are born-digital PDFs |
| `DOCLING_DO_TABLE_STRUCTURE` | `false` | TableFormer off for resume layout |
| `HF_HUB_OFFLINE` | `1` | Block runtime Hugging Face downloads |

Caching behavior:

- **First build** downloads models from Hugging Face once into `/opt/docling/models` (and a BuildKit cache).
- **Code-only rebuilds** (`parser/`, `apps/api/`, `workers/`) reuse the cached model layer — no re-download.
- **BuildKit cache mount** (`docling-models-v2.15`) skips the network even when the model layer must rebuild (e.g. after a `requirements.txt` change), as long as the local BuildKit cache still has the weights.
- **Runtime** never hits Hugging Face. Weights are already on disk; the parse worker loads them into RAM at boot (tens of seconds once per container start — not a download).
- **Upgrading `docling`** should bump the cache mount id in `Dockerfile.api` and rebuild; never reuse model artifacts across unverified Docling versions.
- Scanned / image-only CVs stay on the custom-parser + review path while OCR is disabled.

## Repo layout

```
apps/api          FastAPI
apps/web          React UI
services/matcher  Hybrid match stub
services/parser   Placeholder for Docling pipeline
workers/          parse / match / ingest workers
infra/            Dockerfiles (+ legacy compose include)
parser/           Legacy CV parser prototype
docker-compose.yml  Full-stack Compose (preferred)
```
