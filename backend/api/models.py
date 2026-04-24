"""
FinSight AI — API Models
All Pydantic request/response schemas
"""

from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ── Request Models ────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1000)
    top_k: int = Field(default=8, ge=1, le=20)

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "What are the key risks in HSBC Q3 earnings?",
                "top_k": 8,
            }
        }
    }


class IngestRequest(BaseModel):
    documents: list[dict]
    doc_type: str = "news"


# ── Agent Output Models ───────────────────────────────────────────────────────

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskAnalysis(BaseModel):
    risk_level: RiskLevel
    key_risks: list[str]
    risk_score: float = Field(ge=0.0, le=10.0)
    mitigation_strategies: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str


class SentimentAnalysis(BaseModel):
    overall_sentiment: str
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    key_drivers: list[str]
    market_outlook: str
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str


class PortfolioInsight(BaseModel):
    tickers_mentioned: list[str]
    buy_signals: list[str]
    sell_signals: list[str]
    hold_recommendations: list[str]
    sector_outlook: str
    key_metrics: dict[str, Any]
    executive_summary: str


# ── Response Models ───────────────────────────────────────────────────────────

class AnalyzeResponse(BaseModel):
    query: str
    risk_analysis: RiskAnalysis
    sentiment_analysis: SentimentAnalysis
    portfolio_insight: PortfolioInsight
    overall_recommendation: str
    confidence_score: float
    generated_at: str
    sources_used: int


class RetrieveResult(BaseModel):
    content: str
    metadata: dict


class RetrieveResponse(BaseModel):
    query: str
    results: list[RetrieveResult]
    count: int


class IngestResponse(BaseModel):
    status: str
    doc_count: int


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    vector_store_ready: bool
    total_vectors: int
    environment: str
