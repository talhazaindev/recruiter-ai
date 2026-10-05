# Recruiter AI

Production-oriented ATS shell: **JD → CV ingest (upload / Google Drive) → parse → hybrid match → dashboard → shortlist / review**, with stubs for future AI voice screening.

## Stack

| Layer | Tech |
|---|---|
| Web | React + Vite + TypeScript + Tailwind + TanStack Query + Framer Motion |
| API | FastAPI + Motor (MongoDB) + JWT auth |
| Queue | Redis lists (parse / match / ingest workers) |
| Files | MinIO (S3-compatible) |
| Matcher | services/matcher stub (swap for teammate pipeline) |
| Parser | Stub adapter (PARSER_MODE=stub) or local package (PARSER_MODE=local) |

## Quick start (local)

### 1. Infrastructure

```bash
docker compose -f infra/docker-compose.yml up mongo redis minio -d
```

Defaults in `.env.example`:

- Mongo `mongodb://localhost:27017`
- Redis `redis://localhost:6379/0`
- MinIO `http://localhost:9000` (minioadmin / minioadmin)

### 2. Environment

```bash
cp .env.example .env
```

For local API, set `MONGODB_URI`, `REDIS_URL`, and `S3_ENDPOINT` to localhost hosts.

### 3. API

```bash
cd apps/api
python -m venv .venv
pip install -r requirements.txt
# PowerShell: set PYTHONPATH to apps/api and repo root
uvicorn app.main:app --reload --port 8000
```

Seed admin (auto on startup): `admin@recruiter.ai` / `admin123456`

### 4. Workers

From repo root:

```bash
python workers/parse_worker.py
python workers/match_worker.py
python workers/ingest_worker.py
```

If Redis is down, upload ingest falls back to inline parse+match in the API.

### 5. Web

```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:5173

## Flow

1. Create job and edit JD (must-have skills = hard filters).
2. Upload CVs and/or Drive folder.
3. Watch pipeline progress.
4. Results → shortlist; Review queue for low confidence.
5. AI Call creates screening_calls stub records.

## Google Drive

Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`. Connect from Ingest page.

## Matcher swap

Keep `match_jd_resume(jd, resume)` in `services/matcher` returning hard_filters, score, rank_signals, explanation, matcher_version.

## Full Docker

```bash
docker compose -f infra/docker-compose.yml up --build
```

API :8000 · Web :5173 · MinIO console :9001
