"""
FinSight AI — Data Ingestion Pipeline
Streams financial data from NewsAPI, yfinance, SEC EDGAR into Kafka topics
"""

import json
import os
import time
from datetime import datetime, timedelta

import requests
import yfinance as yf
from kafka import KafkaProducer
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVERS  = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
NEWS_API_KEY   = os.getenv("NEWS_API_KEY")
TICKERS        = ["AAPL", "MSFT", "GOOGL", "JPM", "GS", "HSBA.L", "LLOY.L"]
NEWS_QUERIES   = ["fintech banking UK London", "Federal Reserve interest rates", "HSBC Monzo Revolut", "AI machine learning finance"]
SEC_CIKS       = {"AAPL": "0000320193", "MSFT": "0000789019", "JPM": "0000019617", "GS": "0000886982"}
TOPICS         = {"news": "finsight.news", "prices": "finsight.prices", "filings": "finsight.filings"}


class KafkaPublisher:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode(),
            key_serializer=lambda k: k.encode() if k else None,
            acks="all", retries=3,
        )

    def publish(self, topic: str, key: str, data: dict):
        self.producer.send(topic, key=key, value=data).get(timeout=10)

    def close(self):
        self.producer.flush()
        self.producer.close()


class NewsIngester:
    def __init__(self, pub: KafkaPublisher):
        self.pub = pub

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def fetch(self, query: str) -> list[dict]:
        resp = requests.get("https://newsapi.org/v2/everything", params={
            "q": query, "from": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "sortBy": "publishedAt", "language": "en", "apiKey": NEWS_API_KEY, "pageSize": 50,
        }, timeout=10)
        resp.raise_for_status()
        return resp.json().get("articles", [])

    def ingest(self, queries: list[str]):
        for q in queries:
            for a in self.fetch(q):
                self.pub.publish(TOPICS["news"], q, {
                    "source": a.get("source", {}).get("name"), "title": a.get("title"),
                    "description": a.get("description"), "content": a.get("content"),
                    "url": a.get("url"), "published_at": a.get("publishedAt"),
                    "query": q, "ingested_at": datetime.utcnow().isoformat(),
                })


class MarketPriceIngester:
    def __init__(self, pub: KafkaPublisher):
        self.pub = pub

    def ingest(self, tickers: list[str]):
        for ticker in tickers:
            try:
                hist = yf.Ticker(ticker).history(period="1d", interval="1m")
                if hist.empty:
                    continue
                row = hist.iloc[-1]
                self.pub.publish(TOPICS["prices"], ticker, {
                    "ticker": ticker, "price": round(float(row["Close"]), 4),
                    "volume": int(row["Volume"]), "high": round(float(row["High"]), 4),
                    "low": round(float(row["Low"]), 4), "timestamp": datetime.utcnow().isoformat(),
                })
            except Exception as e:
                logger.warning(f"Price fetch failed {ticker}: {e}")


class SECFilingsIngester:
    def __init__(self, pub: KafkaPublisher):
        self.pub = pub
        self.headers = {"User-Agent": "FinSightAI atharvsatpute777@gmail.com"}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def fetch(self, cik: str) -> list[dict]:
        url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
        data = requests.get(url, headers=self.headers, timeout=10).json()
        filings = data.get("filings", {}).get("recent", {})
        return [{"accession": filings["accessionNumber"][i], "form": filings["form"][i],
                 "date": filings["filingDate"][i]}
                for i in range(min(5, len(filings.get("form", []))))
                if filings["form"][i] in ["10-K", "10-Q", "8-K"]]

    def ingest(self, companies: dict[str, str]):
        for ticker, cik in companies.items():
            try:
                for f in self.fetch(cik):
                    self.pub.publish(TOPICS["filings"], ticker, {
                        "ticker": ticker, "cik": cik,
                        "ingested_at": datetime.utcnow().isoformat(), **f,
                    })
            except Exception as e:
                logger.warning(f"SEC fetch failed {ticker}: {e}")


class IngestionPipeline:
    def __init__(self):
        self.pub = KafkaPublisher()
        self.news = NewsIngester(self.pub)
        self.prices = MarketPriceIngester(self.pub)
        self.filings = SECFilingsIngester(self.pub)

    def run_once(self):
        logger.info("Ingestion cycle starting...")
        self.news.ingest(NEWS_QUERIES)
        self.prices.ingest(TICKERS)
        self.filings.ingest(SEC_CIKS)
        logger.info("Ingestion cycle complete")

    def run_continuous(self, interval: int = 300):
        logger.info(f"Continuous ingestion every {interval}s")
        while True:
            try:
                self.run_once()
            except Exception as e:
                logger.error(f"Cycle error: {e}")
            time.sleep(interval)

    def close(self):
        self.pub.close()


if __name__ == "__main__":
    pipeline = IngestionPipeline()
    try:
        pipeline.run_continuous()
    except KeyboardInterrupt:
        pipeline.close()
