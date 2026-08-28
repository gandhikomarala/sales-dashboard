# ApexSales 360 - Enterprise Revenue Intelligence & Sales Analytics Platform

ApexSales 360 is an enterprise-grade sales performance dashboard, MRR/ARR waterfall forecaster, deal velocity tracker, and automated revenue intelligence suite.

## Architecture
- **Revenue Core**: Real-time MRR/ARR waterfall computations, cohort retention modeling, and win-rate analysis.
- **Pipeline Intelligence**: Multi-stage funnel analysis with weighted forecasting and deal slippage alerting.
- **Rep Performance Matrix**: Individual rep quota attainment leaderboard with territory breakdowns.
- **FastAPI Engine**: High-throughput vectorized financial metrics backend with sub-10ms response times.

## Installation Instructions
```bash
# Clone the repository
git clone git@github.com:gandhikomarala/sales-dashboard.git
cd sales-dashboard

# Backend dependencies
pip install -r backend/requirements.txt

# Frontend dependencies
cd frontend
npm install
```

## Build Instructions
```bash
# Build the production frontend distribution
cd frontend
npm run build

# Build with Docker Compose
cd ..
docker-compose build
```

## Run Instructions
```bash
# Start FastAPI backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Start Frontend Dev Server
cd frontend
npm run dev -- --port 3000

# Run all with Docker Compose
docker-compose up -d
```

## Test Instructions
```bash
# Run backend Pytest suite
pytest backend/tests

# Run frontend Vitest suite
cd frontend && npm test
```
