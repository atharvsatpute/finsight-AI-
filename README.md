# FinSight AI 🧠

> **Autonomous Financial Intelligence Agent** — Production-grade RAG + Multi-Agent system with React dashboard, FastAPI backend, and full MLOps pipeline deployed on AWS EKS via Terraform.

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/atharvsatpute/finsight-ai/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/eks)
[![Terraform](https://img.shields.io/badge/Terraform-1.7-7B42BC?style=flat-square&logo=terraform&logoColor=white)](https://terraform.io)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

---

## Live Demo

> **Ask anything:** *"What are the key risks in HSBC's Q3 report?"* → Risk analysis + sentiment score + portfolio signal in under 3 seconds.

---

## UI Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FinSight AI                                    ● 3 agents live   [Refresh] │
│  INTELLIGENCE PLATFORM                                                       │
│ ─────────────────────────────────────────────────────────────────────────── │
│                                                                              │
│  ANALYSIS          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───┐│
│  > Dashboard       │VECTORS       │ │RAG PRECISION │ │QUERIES TODAY │ │AGT ││
│    Query           │INDEXED       │ │              │ │              │ │SUC ││
│    Reports         │84,291        │ │84%           │ │1,847         │ │98% ││
│                    │+1,240 today  │ │+2.1% week    │ │avg 312ms     │ │    ││
│  SYSTEM            └──────────────┘ └──────────────┘ └──────────────┘ └───┘│
│    Agents          ┌──────────────────────────────────────────────────────┐ │
│    RAG Pipeline    │ Financial intelligence query        [RAG+AGENTS LIVE]│ │
│    MLflow          │ ┌──────────────────────────────────────┐ [Analyze]  │ │
│    Monitoring      │ │ What are HSBC key risks this quarter?│            │ │
│                    │ └──────────────────────────────────────┘            │ │
│  CONFIG            │ [Fintech sentiment] [Rate impact] [Earnings risk]   │ │
│    Data Sources    └──────────────────────────────────────────────────── ┘ │
│    Settings        ┌───────────────────────┐  ┌──────────────────────────┐ │
│                    │ Agent status          │  │ Analysis report          │ │
│  ─────────────     │ ┌─────┐ ┌─────┐ ┌──┐│  │ RISK ANALYSIS            │ │
│  Atharv S.         │ │  R  │ │  S  │ │P ││  │ [HIGH] score: 7.2/10     │ │
│  ML Engineer       │ │Risk │ │Sent │ │Po││  │ Interest rate exposure... │ │
│  84,291 vectors    │ │Run  │ │Run  │ │Id││  │                          │ │
│                    │ └─────┘ └─────┘ └──┘│  │ SENTIMENT ANALYSIS       │ │
│                    │ Query Volume 24H     │  │ positive (+0.42)         │ │
│                    │ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁    │  │                          │ │
│                    └───────────────────── ┘  │ PORTFOLIO SIGNAL         │ │
│                    ┌───────────────────────┐  │ BUY HSBA.L HOLD LLOY   │ │
│                    │ Live data feed  KAFKA │  └──────────────────────── ┘ │
│                    │ ● HSBC Q3 beats...    │                              │
│                    │ ● BoE holds rates...  │  ┌──────────────────────────┐ │
│                    │ ● Monzo 10M users...  │  │ RAG Pipeline Performance │ │
│                    └───────────────────────┘  │ risk-queries    ████ 87% │ │
│                                               │ sentiment       ███  81% │ │
│                                               │ portfolio       ████ 84% │ │
│                                               └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## What It Does

FinSight AI ingests real-time financial data from SEC filings, market prices, and news feeds — indexes it into a FAISS vector store — and runs a coordinated multi-agent pipeline to answer complex financial questions. Every response is a fully structured, typed report covering risk analysis, market sentiment, and portfolio signals, generated in under 3 seconds.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    React Dashboard  (Vite + Tailwind)                │
│     Sidebar · MetricCards · QueryPanel · AgentStatus · ResultPanel   │
│            LiveFeed · PerfChart  —  all wired to useFinSight hook    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │  REST  (Axios → VITE_API_URL)
┌──────────────────────────▼──────────────────────────────────────────┐
│                       FastAPI Backend                                 │
│    POST /analyze  ·  POST /retrieve  ·  POST /ingest  ·  GET /health │
│    GET /metrics   ·  CORS for localhost:5173 + production domain      │
└────────┬──────────────────┬─────────────────────┬────────────────────┘
         │                  │                      │
┌────────▼──────┐  ┌────────▼──────────┐  ┌───────▼──────┐
│  RAG Pipeline │  │  Agent System     │  │  Ingestion   │
│  rag/         │  │  agents/          │  │  ingestion/  │
│  HuggingFace  │  │  LangGraph        │  │  Kafka       │
│  FAISS + S3   │  │  Pydantic AI      │  │  NewsAPI     │
│  MLflow       │  │  Groq LLM         │  │  SEC EDGAR   │
└───────────────┘  └───────────────────┘  └──────────────┘
         │                  │
┌────────▼──────────────────▼──────────────────────────────────────────┐
│                      AWS Infrastructure                               │
│        EKS · S3 · RDS PostgreSQL · ElastiCache · CloudWatch          │
│        All provisioned via Terraform (eu-west-2 — London)            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## How Every Feature Works

### 1. Dashboard Metrics (top row)

The four metric cards — Vectors Indexed, RAG Precision, Queries Today, Agent Success — are populated by polling `GET /health` every 30 seconds via the `useFinSight` hook. The health endpoint reads directly from the live FAISS index (`vector_store.index.ntotal`) and Prometheus counters.

### 2. Financial Intelligence Query Panel

The query panel is the core interaction surface. When a user types a question and clicks Analyze:

```
QueryPanel → useFinSight.analyze() → api.analyze() → POST /analyze
→ FinSightOrchestrator.run()
    ├── _retrieve()         RAG: top-10 chunks from FAISS
    ├── _risk()             RiskAgent: Pydantic AI → Groq → RiskAnalysis schema
    ├── _sentiment()        SentimentAgent: Pydantic AI → Groq → SentimentAnalysis schema
    ├── _portfolio()        PortfolioAgent: synthesises risk + sentiment → PortfolioInsight
    └── _compile()          FinalReport assembled, confidence averaged
← Typed JSON response → ResultPanel renders risk, sentiment, portfolio cards
```

All agent outputs are validated by Pydantic schemas — if Groq returns malformed JSON, retries fire automatically via `tenacity` (3 attempts, exponential backoff).

### 3. Agent Status Panel

Shows real-time state of all three agents: Risk, Sentiment, Portfolio. The `useFinSight` hook drives a simulated animation that lights agents up in sequence (200ms → 800ms → 1600ms delays) while the real API call is in flight. On success, all three show "Done". On failure, all show "Error" with the message surfaced in ResultPanel.

### 4. Result Panel

Renders the structured `FinalReport` from the backend:

- **Risk section** — risk level badge (low/medium/high/critical), score bar (0–10), key risks list, summary text
- **Sentiment section** — sentiment label + score (−1 to +1), market outlook, key drivers
- **Portfolio section** — BUY / HOLD / SELL signal pills per ticker, executive summary

All data is typed end-to-end: `RiskAnalysis`, `SentimentAnalysis`, `PortfolioInsight` Pydantic models on the backend map directly to the React component props.

### 5. Live Data Feed

Simulates the Kafka stream from `ingestion/pipeline.py`. In production, this connects to a WebSocket endpoint that consumes from `finsight.news`, `finsight.prices`, and `finsight.filings` Kafka topics and pushes events to the browser in real time. New items animate in at the top of the feed list.

### 6. RAG Pipeline Performance Chart

Bar charts built with Recharts showing retrieval precision per query type (risk, sentiment, portfolio, SEC filing, macro). Precision scores are logged to MLflow via `evaluate_retrieval()` in `rag/pipeline.py` and surfaced through `GET /metrics` (Prometheus). The 24-hour volume chart shows query count per hour, with the last 4 hours highlighted in accent green.

### 7. Query Chips

Pre-set query shortcuts: "Fintech sentiment", "Rate impact", "Earnings risk", "London outlook". Clicking a chip sets the query text AND immediately calls `analyze()` — so one click fires the full pipeline.

---

## Data Flow — End to End

```
1. INGEST (continuous, every 5 minutes)
   ingestion/pipeline.py
   ├── NewsIngester     → NewsAPI → Kafka topic: finsight.news
   ├── MarketPriceIngester → yfinance → Kafka topic: finsight.prices
   └── SECFilingsIngester → SEC EDGAR → Kafka topic: finsight.filings

2. INDEX (background task via POST /ingest)
   rag/pipeline.py
   ├── DocumentProcessor — splits text into 512-char chunks with 64-char overlap
   ├── EmbeddingModel    — HuggingFace all-mpnet-base-v2, normalized, batch=32
   ├── LangchainFAISS    — L2 distance index, persisted to AWS S3
   └── MLflow            — logs chunk count, total vectors, precision metrics

3. QUERY (on user request)
   agents/orchestrator.py (LangGraph)
   ├── retrieve   — top-10 FAISS chunks, score threshold < 1.2
   ├── risk       — RiskAgent (Pydantic AI + Groq)
   ├── sentiment  — SentimentAgent (Pydantic AI + Groq)
   ├── portfolio  — PortfolioAgent (synthesises risk + sentiment)
   └── compile    — FinalReport, confidence = avg(risk.conf, sentiment.conf)

4. RESPOND
   FastAPI → JSON → Axios → useFinSight hook → React components
```

---

## Why We Chose Each Technology

| Technology | Why |
|---|---|
| **Groq LLM** | 500+ tokens/sec via custom LPU hardware. Agentic pipelines make 3–5 LLM calls per query — speed multiplies across every call. At 1M+ daily transactions, standard GPU APIs would bottleneck. |
| **Pydantic AI** | Eliminates an entire class of production bugs. Every agent output is schema-validated — no raw string parsing, no silent hallucinations reaching the database. |
| **LangGraph** | Stateful multi-agent orchestration with explicit node/edge graph. Easier to debug than LangChain chains, supports parallel agent execution, and has built-in retry logic. |
| **FAISS** | In-process vector search with no network hop. Persisted to S3 so it survives restarts. At sub-100k vectors, FAISS on CPU outperforms Pinecone on latency. |
| **HuggingFace all-mpnet-base-v2** | Best-in-class semantic similarity for financial text. Fine-tunable on domain-specific data. Runs on CPU — no GPU cost for inference. |
| **Kafka** | Decouples ingestion from indexing. Sources can produce at different rates. Consumer lag is visible, backpressure is natural, and topics are replayable. |
| **Terraform** | Infrastructure as code — if the EKS cluster dies at 2am, `terraform apply` rebuilds the entire stack in under 10 minutes. No manual console clicking. |
| **Airflow DAGs** | Scheduled retraining with drift detection. If RAG precision drops below 75%, the DAG auto-retrains embeddings and rebuilds the FAISS index — no human intervention. |
| **Prometheus + Grafana** | Production ML needs observable metrics: request latency, agent success rate, RAG precision, vector count. Grafana dashboards surface all of these live. |
| **React + Vite + Tailwind** | Vite's HMR makes frontend development instant. Tailwind's utility classes with CSS variables enable the dark terminal aesthetic without a design system overhead. |

---

## Project Structure

```
finsight-ai/
│
├── frontend/                     # React + Vite dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx       # Left nav, agent avatar, vector count
│   │   │   ├── MetricCard.jsx    # Reusable metric display card
│   │   │   ├── QueryPanel.jsx    # Query input, chips, analyze button
│   │   │   ├── AgentStatus.jsx   # Risk/Sentiment/Portfolio agent cards
│   │   │   ├── ResultPanel.jsx   # Structured report display
│   │   │   ├── LiveFeed.jsx      # Kafka-style live data feed
│   │   │   └── PerfChart.jsx     # Recharts RAG precision + volume charts
│   │   ├── hooks/
│   │   │   └── useFinSight.js    # All state + API calls + agent animation
│   │   ├── services/
│   │   │   └── api.js            # Axios client, auth header, error handling
│   │   ├── pages/
│   │   │   └── Dashboard.jsx     # Main layout, grid composition
│   │   ├── styles/
│   │   │   └── globals.css       # CSS vars, animations, scrollbar
│   │   ├── App.jsx               # Root component, Sidebar + Dashboard
│   │   └── main.jsx              # React DOM entry point
│   ├── index.html                # Vite HTML entry, Google Fonts link
│   ├── vite.config.js            # Dev server proxy → localhost:8000
│   ├── tailwind.config.js        # Custom colors, fonts (Syne + DM Mono)
│   └── package.json              # React, Recharts, Lucide, Axios, clsx
│
├── backend/                      # Python FastAPI backend
│   ├── api/
│   │   ├── main.py               # FastAPI app, all routes, CORS, lifespan
│   │   └── models.py             # Pydantic request/response schemas
│   ├── agents/
│   │   └── orchestrator.py       # LangGraph pipeline + 3 Pydantic AI agents
│   ├── rag/
│   │   └── pipeline.py           # Embeddings, FAISS, S3, MLflow tracking
│   ├── ingestion/
│   │   └── pipeline.py           # Kafka producer, NewsAPI, yfinance, SEC
│   ├── mlops/
│   │   └── dag_retraining.py     # Airflow DAG: ingest→eval→retrain→rebuild
│   ├── tests/
│   │   └── test_core.py          # Unit tests: processor, schemas, API models
│   ├── requirements.txt          # All Python dependencies pinned
│   └── Dockerfile                # Multi-stage build, non-root user
│
├── infra/
│   ├── terraform/
│   │   └── main.tf               # VPC, EKS, S3, RDS, ElastiCache, IAM, SNS
│   └── k8s/
│       ├── deployment.yaml       # API + Frontend deployments, health probes
│       └── service.yaml          # LoadBalancer services + finsight namespace
│
├── monitoring/
│   └── prometheus.yml            # Scrape config: API metrics, Kafka, node
│
├── .github/
│   └── workflows/
│       └── cicd.yml              # Test → Build → ECR push → EKS deploy
│
├── docker-compose.yml            # Zookeeper, Kafka, Redis, Postgres, MLflow,
│                                 # Prometheus, Grafana, API, Ingestion worker
├── .env.example                  # All environment variables documented
└── README.md
```

---

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose
- AWS CLI configured (for cloud deployment)

### 1. Clone and configure

```bash
git clone https://github.com/atharvsatpute/finsight-ai.git
cd finsight-ai
cp .env.example .env
# Open .env and add your API keys
```

### 2. Start backend services

```bash
# Start Kafka, Redis, PostgreSQL, MLflow, Prometheus, Grafana
docker-compose up -d zookeeper kafka redis postgres mlflow prometheus grafana

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start FastAPI
uvicorn api.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### 3. Start the React dashboard

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### 4. Start data ingestion

```bash
cd backend
python -m ingestion.pipeline
# Starts streaming: NewsAPI → Kafka → FAISS every 5 minutes
```

### 5. Make your first query

Open `http://localhost:5173`, type any financial question, and click **Analyze**. Watch all three agents activate and the structured report appear.

---

## Environment Variables

```bash
# LLM + ML
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_API_KEY=your_hf_key

# Data sources
NEWS_API_KEY=your_newsapi_key
SEC_API_KEY=your_sec_api_key
ALPHA_VANTAGE_KEY=your_alpha_vantage_key

# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=eu-west-2
S3_BUCKET=finsight-ai-prod

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Database
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://postgres:password@localhost:5432/finsight

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000

# App
APP_ENV=development
FINSIGHT_API_KEY=dev-key-123

# Frontend
VITE_API_URL=http://localhost:8000
VITE_API_KEY=dev-key-123
```

---

## API Reference

| Method | Endpoint | Description | Called by |
|---|---|---|---|
| `GET` | `/health` | Health check, vector count, env | `useFinSight` hook every 30s |
| `POST` | `/analyze` | Full multi-agent analysis | `QueryPanel` on Analyze click |
| `POST` | `/retrieve` | RAG vector search only | Direct RAG exploration |
| `POST` | `/ingest` | Add documents to vector store | Ingestion pipeline, `/ingest` API |
| `GET` | `/metrics` | Prometheus metrics | Prometheus scraper |

### Sample request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "What are key risks in HSBC Q3 earnings?", "top_k": 8}'
```

### Sample response

```json
{
  "query": "What are key risks in HSBC Q3 earnings?",
  "risk_analysis": {
    "risk_level": "medium",
    "risk_score": 6.2,
    "key_risks": ["Interest rate exposure", "Regulatory compliance", "Credit risk"],
    "confidence": 0.84,
    "summary": "Moderate risk driven by rate sensitivity..."
  },
  "sentiment_analysis": {
    "overall_sentiment": "positive",
    "sentiment_score": 0.42,
    "market_outlook": "Cautiously optimistic",
    "confidence": 0.78
  },
  "portfolio_insight": {
    "buy_signals": ["HSBA.L"],
    "hold_recommendations": ["LLOY.L"],
    "executive_summary": "Moderate buy on dip below 650p..."
  },
  "confidence_score": 0.81,
  "sources_used": 9,
  "generated_at": "2025-04-23T10:00:00Z"
}
```

---

## MLOps Pipeline

The Airflow DAG (`mlops/dag_retraining.py`) runs daily at 2am:

```
start
  └── ingest_data          Pull fresh news, prices, SEC filings
        └── evaluate_rag   Check retrieval precision on benchmark queries
              └── drift_check
                    ├── [precision < 75%] retrain_embeddings
                    │         └── rebuild_vector_store
                    │                   └── notify → end
                    └── [precision OK]  skip_retrain
                                          └── notify → end
```

---

## Deployment

### AWS via Terraform

```bash
cd infra/terraform
terraform init
terraform plan -var="db_password=yourpassword"
terraform apply
```

### Docker Build and Push

```bash
cd backend
docker build -t finsight-ai .
docker tag finsight-ai:latest <ECR_URL>/finsight-ai:latest
docker push <ECR_URL>/finsight-ai:latest
```

### Kubernetes Deploy

```bash
kubectl apply -f infra/k8s/
kubectl rollout status deployment/finsight-api -n finsight
kubectl rollout status deployment/finsight-frontend -n finsight
```

---

## Monitoring

| Service | URL | Purpose |
|---|---|---|
| React Dashboard | http://localhost:5173 | Main application UI |
| API Docs | http://localhost:8000/docs | FastAPI Swagger UI |
| Grafana | http://localhost:3001 | Metrics dashboards (admin/admin) |
| Prometheus | http://localhost:9090 | Raw metrics scraping |
| MLflow | http://localhost:5000 | Experiment tracking |

---

## Adding a New Data Source

1. Create `backend/ingestion/your_source.py` following the `NewsIngester` pattern
2. Add it to `IngestionPipeline.run_once()` in `ingestion/pipeline.py`
3. Add the Kafka topic to `.env`
4. Ensure your document dict has `content`, `source`, `doc_type`, `published_at`
5. The RAG pipeline picks it up automatically on next ingest cycle

---

## Author

**Atharv Satpute** — ML Engineer
📩 atharvsatpute777@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/atharvsatpute)
☁️ AWS Certified AI Practitioner + ML Engineer Associate

---

## License

MIT — see [LICENSE](LICENSE) for details.
