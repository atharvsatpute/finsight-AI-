"""
FinSight AI — RAG Pipeline
HuggingFace embeddings → FAISS → LangChain retrieval → S3 persistence → MLflow tracking
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

import boto3
import mlflow
import numpy as np
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS as LangchainFAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET      = os.getenv("S3_BUCKET", "finsight-ai-prod")
MLFLOW_URI     = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EMBEDDING_MODEL= "sentence-transformers/all-mpnet-base-v2"


class EmbeddingModel:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
        )
        logger.info(f"Embeddings loaded: {EMBEDDING_MODEL}")


class S3VectorStore:
    def __init__(self):
        self.bucket = S3_BUCKET
        self.s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "eu-west-2"))

    def save(self, store: LangchainFAISS):
        with tempfile.TemporaryDirectory() as tmp:
            store.save_local(tmp)
            for fname in ["index.faiss", "index.pkl"]:
                self.s3.upload_file(str(Path(tmp) / fname), self.bucket, f"faiss/{fname}")
        logger.info("FAISS index saved to S3")

    def load(self, embeddings) -> Optional[LangchainFAISS]:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                for fname in ["index.faiss", "index.pkl"]:
                    self.s3.download_file(self.bucket, f"faiss/{fname}", str(Path(tmp) / fname))
                store = LangchainFAISS.load_local(tmp, embeddings, allow_dangerous_deserialization=True)
                logger.info("FAISS index loaded from S3")
                return store
        except Exception as e:
            logger.warning(f"Could not load FAISS from S3: {e}")
            return None

    def exists(self) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key="faiss/index.faiss")
            return True
        except Exception:
            return False


class DocumentProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=64,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def process(self, raw_docs: list[dict]) -> list[Document]:
        docs = []
        for d in raw_docs:
            text = d.get("content") or d.get("description") or d.get("title", "")
            if not text or len(text.strip()) < 50:
                continue
            for chunk in self.splitter.split_text(text):
                docs.append(Document(
                    page_content=chunk,
                    metadata={k: d.get(k, "") for k in ["source", "title", "url", "published_at", "ticker", "doc_type"]},
                ))
        logger.info(f"Processed {len(raw_docs)} docs → {len(docs)} chunks")
        return docs


class RAGPipeline:
    def __init__(self):
        mlflow.set_tracking_uri(MLFLOW_URI)
        mlflow.set_experiment("finsight-rag")
        self.embedding_model = EmbeddingModel()
        self.s3_store = S3VectorStore()
        self.processor = DocumentProcessor()
        self.vector_store: Optional[LangchainFAISS] = None
        self._init_store()

    def _init_store(self):
        if self.s3_store.exists():
            self.vector_store = self.s3_store.load(self.embedding_model.embeddings)

    def ingest(self, raw_docs: list[dict]) -> dict:
        with mlflow.start_run(run_name="rag-ingest"):
            mlflow.log_param("num_raw_docs", len(raw_docs))
            docs = self.processor.process(raw_docs)
            if not docs:
                return {"indexed": 0}
            if self.vector_store is None:
                self.vector_store = LangchainFAISS.from_documents(docs, self.embedding_model.embeddings)
            else:
                self.vector_store.add_documents(docs)
            self.s3_store.save(self.vector_store)
            total = self.vector_store.index.ntotal
            mlflow.log_metric("chunks_indexed", len(docs))
            mlflow.log_metric("total_vectors", total)
            return {"indexed": len(docs), "total_vectors": total}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=5))
    def retrieve(self, query: str, top_k: int = 8) -> list[Document]:
        if self.vector_store is None:
            return []
        results = self.vector_store.similarity_search_with_score(query, k=top_k)
        return [doc for doc, score in results if score < 1.2]

    def get_context_string(self, query: str, top_k: int = 8) -> str:
        docs = self.retrieve(query, top_k)
        if not docs:
            return "No relevant context found."
        parts = [f"[Source {i+1}: {d.metadata.get('source','?')}]\n{d.metadata.get('title','')}\n{d.page_content}" for i, d in enumerate(docs)]
        return "\n---\n".join(parts)

    def evaluate_retrieval(self, queries: list[str], keywords: list[list[str]]) -> dict:
        with mlflow.start_run(run_name="rag-eval"):
            precisions = []
            for q, kws in zip(queries, keywords):
                docs = self.retrieve(q, top_k=5)
                text = " ".join(d.page_content for d in docs).lower()
                hits = sum(1 for kw in kws if kw.lower() in text)
                precisions.append(hits / len(kws) if kws else 0)
            avg = float(np.mean(precisions))
            mlflow.log_metric("avg_retrieval_precision", avg)
            return {"avg_precision": avg, "per_query": precisions}
