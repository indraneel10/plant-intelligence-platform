# Plant Intelligence App

This is the user-facing application layer for the Plant Intelligence Platform.

It consumes the existing FastAPI contracts for plants and monitoring and provides the first AI Copilot experience.

## Run

Backend:
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:
```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

The Vite server proxies /plants and /monitor to the FastAPI backend at http://127.0.0.1:8000.

## Direction

The Copilot is intentionally an application-layer concern. It should not own plant-control logic. The next step is to replace the local context response with a backend AI orchestration endpoint that can call platform tools such as plant state, sensor history, vision results, decisions and irrigation history.
