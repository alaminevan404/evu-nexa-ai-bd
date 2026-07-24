# EVU NEXA AI - Production-Grade Binary Market Analysis Platform

EVU NEXA AI is a state-of-the-art, high-performance Binary Option & Financial Market Analysis Platform. It features real-time multi-asset technical breakdown, Smart Money Concepts (SMC) pattern recognition, institutional liquidity analysis, and multi-timeframe indicator synthesis across 200+ configurable analysis modules.

## Architecture Stack
- **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.0 (Async), AsyncPG, Pydantic v2, Redis 7, pandas, pandas_ta.
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS (Obsidian Theme), Framer Motion, Lightweight Charts, Zustand.
- **Database**: PostgreSQL 15, Redis 7.
- **Security**: Single-gate License Key verification with dynamic SHA-256 WebGL/Canvas Hardware Client Fingerprinting.
- **Notifications**: Telegram Bot Webhook & HTML Signal Dispatcher (`@et_evu`).

## Seed License Keys
- **Master Admin Key**: `NEXA-ADMIN-9999-MASTER`
- **Demo Pro Key**: `NEXA-PRO-89F2-44A1-9B2C`

## Running via Docker Compose
```bash
docker-compose up --build -d
```
The web application will be accessible at `http://localhost`.

## Local Development Boot
1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:5173`.
