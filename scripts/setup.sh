#!/bin/bash
# FinSight AI — One-command setup script
set -e

echo ""
echo "========================================"
echo "  FinSight AI — Project Setup"
echo "========================================"
echo ""

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3.11+ is required."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js 18+ is required."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required."; exit 1; }

echo "[1/6] Copying .env file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  Created .env — please fill in your API keys before continuing!"
  echo "  Press Enter when ready..."
  read
else
  echo "  .env already exists — skipping"
fi

echo ""
echo "[2/6] Starting Docker services..."
docker compose up -d zookeeper kafka redis postgres mlflow prometheus grafana
echo "  Waiting 20 seconds for services to start..."
sleep 20

echo ""
echo "[3/6] Creating Kafka topics..."
docker compose exec -T kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic finsight.news \
  --partitions 3 --replication-factor 1 2>/dev/null || true

docker compose exec -T kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic finsight.prices \
  --partitions 3 --replication-factor 1 2>/dev/null || true

docker compose exec -T kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic finsight.filings \
  --partitions 3 --replication-factor 1 2>/dev/null || true
echo "  Kafka topics created"

echo ""
echo "[4/6] Installing Python dependencies..."
cd backend
pip install -r requirements.txt -q
cd ..
echo "  Python packages installed"

echo ""
echo "[5/6] Installing Node dependencies..."
cd frontend
npm install --silent
cd ..
echo "  Node packages installed"

echo ""
echo "[6/6] Setup complete!"
echo ""
echo "========================================"
echo "  To run FinSight AI:"
echo ""
echo "  Terminal 1 — Backend:"
echo "    cd backend && uvicorn api.main:app --reload --port 8000"
echo ""
echo "  Terminal 2 — Frontend:"
echo "    cd frontend && npm run dev"
echo ""
echo "  Terminal 3 — Data ingestion:"
echo "    cd backend && python -m ingestion.pipeline"
echo ""
echo "  Open: http://localhost:5173"
echo "  API:  http://localhost:8000/docs"
echo "  MLflow: http://localhost:5000"
echo "  Grafana: http://localhost:3001 (admin/admin)"
echo "========================================"
echo ""
