# GovData Insight - Deployment Guide

## Prerequisites
- Docker and Docker Compose
- Node 18+ and Python 3.11+ (optional for local dev without Docker)

## Quick start (Docker Compose)

```bash
# from repository root
docker compose up --build -d
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

The frontend is built with `VITE_API_URL=http://backend:8000` and served by nginx. The backend runs FastAPI with Uvicorn.

## Environment
- Frontend reads API base from `VITE_API_URL`.
- Windows PowerShell example:
```powershell
$env:VITE_API_URL="http://localhost:8000"; npm run dev
```

## Local development (without Docker)
### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm ci
# optional: set API URL
# PowerShell: $env:VITE_API_URL="http://localhost:8000"
npm run dev
```

## Production (containers)
- Backend image: build from `backend/` and expose port 8000.
- Frontend image: build from `frontend/` with `--build-arg VITE_API_URL=...` and serve via nginx on port 80.

## Notes
- CORS is open (`*`) in `backend/app.py`. Restrict to your domain(s) for production.
- Point your domain to the frontend; ensure it can reach the backend URL set in `VITE_API_URL`.
