# BoostCoach API

Rocket League AI Coaching Platform - MVP Backend

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run server
python app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### Replay Management
- `POST /api/replays/upload` — Upload .replay file and generate coaching report
- `GET /api/replays` — List user's past analyses
- `GET /api/replays/<id>` — Get specific analysis + coaching report

### Interactive Coaching
- `POST /api/analyses/<id>/ask` — Ask a question about the match
- `GET /api/analyses/<id>/conversation` — Get full Q&A history

### Health
- `GET /health` — Check server status

## Architecture

```
Upload .replay
    ↓
Carball Parser (Python library)
    ↓
Parse match data (goals, players, stats, etc)
    ↓
Claude API (generates coaching report)
    ↓
Store in SQLite
    ↓
Return to user
    ↓
User asks Q&A questions
    ↓
Claude API (context-aware responses)
    ↓
Store conversations
```

## Database

SQLite database (`boostcoach.db`) with 3 tables:
- `users` — User accounts (auth TBD)
- `analyses` — Replay processing results + coaching reports
- `conversations` — Q&A message history

## Next Steps

1. ✅ Backend skeleton + core pipeline
2. ⏳ Auth implementation (JWT)
3. ⏳ Frontend (React/Vue)
4. ⏳ Deployment (Railway/Render)
5. ⏳ Beta testing with real players
6. ⏳ Iterate based on feedback

## Notes

- Auth is stubbed (placeholder only) — implement after core pipeline works
- File storage is local disk (upgrade to S3 later)
- Database is SQLite (upgrade to Postgres after MVP)
