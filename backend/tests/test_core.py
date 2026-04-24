"""FinSight AI — Core Tests"""
import pytest
from unittest.mock import MagicMock, patch
from langchain.docstore.document import Document
from agents.orchestrator import RiskAnalysis, SentimentAnalysis, RiskLevel, AgentState
from rag.pipeline import DocumentProcessor


class TestDocumentProcessor:
    def setup_method(self):
        self.proc = DocumentProcessor()

    def test_processes_valid_doc(self):
        docs = [{"content": "HSBC reported strong Q3 earnings with revenue up 12% driven by net interest income growth in UK markets.", "source": "Reuters", "title": "HSBC Q3"}]
        result = self.proc.process(docs)
        assert len(result) >= 1
        assert isinstance(result[0], Document)
        assert result[0].metadata["source"] == "Reuters"

    def test_skips_short_docs(self):
        assert self.proc.process([{"content": "Short.", "source": "test"}]) == []

    def test_uses_description_fallback(self):
        docs = [{"description": "This is a long enough description about financial markets and banking regulations in the UK.", "source": "test"}]
        assert len(self.proc.process(docs)) >= 1

    def test_chunks_long_docs(self):
        docs = [{"content": "Long financial paragraph. " * 100, "source": "test"}]
        assert len(self.proc.process(docs)) > 1


class TestAgentSchemas:
    def test_risk_analysis_valid(self):
        r = RiskAnalysis(
            risk_level=RiskLevel.HIGH, key_risks=["rate risk"], risk_score=7.5,
            mitigation_strategies=["hedge"], confidence=0.85, summary="High risk"
        )
        assert r.risk_score == 7.5
        assert 0 <= r.confidence <= 1

    def test_risk_score_out_of_range(self):
        with pytest.raises(Exception):
            RiskAnalysis(risk_level=RiskLevel.LOW, key_risks=[], risk_score=15.0,
                         mitigation_strategies=[], confidence=0.5, summary="x")

    def test_sentiment_score_range(self):
        s = SentimentAnalysis(
            overall_sentiment="positive", sentiment_score=0.6,
            key_drivers=["earnings"], market_outlook="bullish", confidence=0.8, summary="ok"
        )
        assert -1.0 <= s.sentiment_score <= 1.0

    def test_agent_state_defaults(self):
        state = AgentState(query="test query")
        assert state.context == ""
        assert state.risk_analysis is None
        assert state.error is None


class TestAPIModels:
    def test_health_response(self):
        from api.models import HealthResponse
        h = HealthResponse(status="healthy", version="1.0.0",
                           timestamp="2024-01-01T00:00:00", vector_store_ready=True,
                           total_vectors=1000, environment="development")
        assert h.status == "healthy"
        assert h.total_vectors == 1000

    def test_query_request_validation(self):
        from api.models import QueryRequest
        q = QueryRequest(query="What are HSBC risks?")
        assert q.top_k == 8

    def test_query_request_min_length(self):
        from api.models import QueryRequest
        with pytest.raises(Exception):
            QueryRequest(query="Hi")
