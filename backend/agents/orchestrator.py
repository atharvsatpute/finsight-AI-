"""
FinSight AI — Multi-Agent Orchestrator
LangGraph pipeline: RAG → Risk Agent → Sentiment Agent → Portfolio Agent → Report
"""

import os
from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from langgraph.graph import END, StateGraph
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


# ── Output Schemas ────────────────────────────────────────────────────────────

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
    key_metrics: dict
    executive_summary: str


class FinalReport(BaseModel):
    query: str
    risk_analysis: RiskAnalysis
    sentiment_analysis: SentimentAnalysis
    portfolio_insight: PortfolioInsight
    overall_recommendation: str
    confidence_score: float
    generated_at: str
    sources_used: int


# ── Agent State ───────────────────────────────────────────────────────────────

class AgentState(BaseModel):
    query: str
    context: str = ""
    risk_analysis: Optional[RiskAnalysis] = None
    sentiment_analysis: Optional[SentimentAnalysis] = None
    portfolio_insight: Optional[PortfolioInsight] = None
    final_report: Optional[FinalReport] = None
    error: Optional[str] = None


# ── Individual Agents ─────────────────────────────────────────────────────────

class RiskAgent:
    SYSTEM = """You are a senior financial risk analyst at a London investment bank.
Analyze financial context and identify key risks precisely.
Focus on: market risk, credit risk, liquidity risk, regulatory risk (PRA/FCA), macro risk.
Return a structured, calibrated risk assessment."""

    def __init__(self):
        self.agent = Agent(model=f"groq:{GROQ_MODEL}", result_type=RiskAnalysis, system_prompt=self.SYSTEM)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    async def run(self, query: str, context: str) -> RiskAnalysis:
        result = await self.agent.run(f"Query: {query}\n\nContext:\n{context}\n\nProvide risk analysis.")
        logger.info(f"Risk: {result.data.risk_level} | score={result.data.risk_score}")
        return result.data


class SentimentAgent:
    SYSTEM = """You are a quantitative sentiment analyst specialising in NLP-driven financial analysis.
Analyse news, filings, and market data to determine sentiment and investor psychology.
Return a calibrated score: -1 (extreme bearish) to +1 (extreme bullish)."""

    def __init__(self):
        self.agent = Agent(model=f"groq:{GROQ_MODEL}", result_type=SentimentAnalysis, system_prompt=self.SYSTEM)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    async def run(self, query: str, context: str) -> SentimentAnalysis:
        result = await self.agent.run(f"Query: {query}\n\nContext:\n{context}\n\nAnalyse sentiment.")
        logger.info(f"Sentiment: {result.data.overall_sentiment} | score={result.data.sentiment_score:.2f}")
        return result.data


class PortfolioAgent:
    SYSTEM = """You are a portfolio manager at a quantitative hedge fund in London.
Synthesise risk and sentiment into actionable portfolio recommendations.
Be specific — give buy/sell/hold signals per ticker with clear rationale."""

    def __init__(self):
        self.agent = Agent(model=f"groq:{GROQ_MODEL}", result_type=PortfolioInsight, system_prompt=self.SYSTEM)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    async def run(self, query: str, context: str, risk: RiskAnalysis, sentiment: SentimentAnalysis) -> PortfolioInsight:
        prompt = f"""Query: {query}
Context (excerpt): {context[:800]}
Risk: {risk.risk_level} ({risk.risk_score}/10) — {', '.join(risk.key_risks[:3])}
Sentiment: {sentiment.overall_sentiment} ({sentiment.sentiment_score:.2f}) — {sentiment.market_outlook}
Generate portfolio-level investment insights."""
        result = await self.agent.run(prompt)
        logger.info(f"Portfolio: {len(result.data.buy_signals)} buy signals")
        return result.data


# ── LangGraph Orchestrator ────────────────────────────────────────────────────

class FinSightOrchestrator:
    """Coordinates all agents in a LangGraph pipeline."""

    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline
        self.risk_agent = RiskAgent()
        self.sentiment_agent = SentimentAgent()
        self.portfolio_agent = PortfolioAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        g = StateGraph(AgentState)
        g.add_node("retrieve",          self._retrieve)
        g.add_node("risk_analysis",     self._risk)
        g.add_node("sentiment_analysis",self._sentiment)
        g.add_node("portfolio_analysis",self._portfolio)
        g.add_node("compile",           self._compile)
        g.set_entry_point("retrieve")
        g.add_edge("retrieve",           "risk_analysis")
        g.add_edge("retrieve",           "sentiment_analysis")
        g.add_edge("risk_analysis",      "portfolio_analysis")
        g.add_edge("sentiment_analysis", "portfolio_analysis")
        g.add_edge("portfolio_analysis", "compile")
        g.add_edge("compile",            END)
        return g.compile()

    async def _retrieve(self, state: AgentState) -> AgentState:
        ctx = self.rag.get_context_string(state.query, top_k=10)
        return state.model_copy(update={"context": ctx})

    async def _risk(self, state: AgentState) -> AgentState:
        risk = await self.risk_agent.run(state.query, state.context)
        return state.model_copy(update={"risk_analysis": risk})

    async def _sentiment(self, state: AgentState) -> AgentState:
        sent = await self.sentiment_agent.run(state.query, state.context)
        return state.model_copy(update={"sentiment_analysis": sent})

    async def _portfolio(self, state: AgentState) -> AgentState:
        if not state.risk_analysis or not state.sentiment_analysis:
            return state
        port = await self.portfolio_agent.run(
            state.query, state.context,
            state.risk_analysis, state.sentiment_analysis,
        )
        return state.model_copy(update={"portfolio_insight": port})

    async def _compile(self, state: AgentState) -> AgentState:
        if not all([state.risk_analysis, state.sentiment_analysis, state.portfolio_insight]):
            return state.model_copy(update={"error": "One or more agents failed"})
        confidence = round((state.risk_analysis.confidence + state.sentiment_analysis.confidence) / 2, 3)
        report = FinalReport(
            query=state.query,
            risk_analysis=state.risk_analysis,
            sentiment_analysis=state.sentiment_analysis,
            portfolio_insight=state.portfolio_insight,
            overall_recommendation=state.portfolio_insight.executive_summary,
            confidence_score=confidence,
            generated_at=datetime.utcnow().isoformat(),
            sources_used=len(state.context.split("---")),
        )
        return state.model_copy(update={"final_report": report})

    async def run(self, query: str) -> FinalReport:
        state = AgentState(query=query)
        final = await self.graph.ainvoke(state)
        if final.get("error"):
            raise RuntimeError(final["error"])
        return final["final_report"]
