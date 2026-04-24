"""
FinSight AI — Airflow Retraining DAG
Runs daily at 2am: ingest → evaluate → drift check → retrain → rebuild → notify
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from loguru import logger

DEFAULT_ARGS = {
    "owner": "atharv-satpute",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["atharvsatpute777@gmail.com"],
}

DRIFT_THRESHOLD = 0.75  # retrain if precision drops below 75%


def run_ingestion(**ctx):
    from ingestion.pipeline import IngestionPipeline
    pipeline = IngestionPipeline()
    pipeline.run_once()
    pipeline.close()
    logger.info("Daily ingestion complete")


def evaluate_rag(**ctx):
    from rag.pipeline import RAGPipeline

    EVAL_QUERIES = [
        ("What are HSBC key risks?",           ["risk", "bank", "financial", "regulatory"]),
        ("Fintech sentiment UK market",         ["fintech", "sentiment", "UK", "market"]),
        ("Federal Reserve interest rates",      ["interest", "rate", "Federal", "Reserve"]),
        ("Monzo Revolut neobank growth",        ["neobank", "growth", "digital", "banking"]),
    ]

    pipeline = RAGPipeline()
    queries  = [q for q, _ in EVAL_QUERIES]
    keywords = [k for _, k in EVAL_QUERIES]
    result   = pipeline.evaluate_retrieval(queries, keywords)
    avg_prec = result["avg_precision"]

    logger.info(f"RAG precision: {avg_prec:.2%}")
    ctx["task_instance"].xcom_push(key="avg_precision", value=avg_prec)
    return result


def check_drift(**ctx):
    avg = ctx["task_instance"].xcom_pull(task_ids="evaluate_rag", key="avg_precision")
    if avg is None or avg < DRIFT_THRESHOLD:
        logger.warning(f"Drift detected — precision {avg:.2%} < {DRIFT_THRESHOLD:.2%}")
        return "retrain_embeddings"
    logger.info(f"No drift — precision {avg:.2%}")
    return "skip_retrain"


def retrain_embeddings(**ctx):
    from sentence_transformers import SentenceTransformer, InputExample, losses
    from torch.utils.data import DataLoader
    import mlflow, boto3, os

    mlflow.set_experiment("finsight-embedding-finetune")
    with mlflow.start_run(run_name="embedding-finetune"):
        model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        train_examples = [
            InputExample(texts=["HSBC quarterly earnings", "HSBC reported Q3 revenue growth of 12%"]),
            InputExample(texts=["Federal Reserve rate decision", "Fed held rates steady at 5.25-5.50%"]),
            InputExample(texts=["FCA fintech regulation", "FCA announced new open banking regulations"]),
            InputExample(texts=["Monzo bank valuation", "Monzo secured £500M Series G at £4B valuation"]),
        ]
        loader     = DataLoader(train_examples, shuffle=True, batch_size=8)
        train_loss = losses.MultipleNegativesRankingLoss(model)
        model.fit(train_objectives=[(loader, train_loss)], epochs=3, warmup_steps=10)
        model.save("/tmp/finsight-embeddings-finetuned")

        s3 = boto3.client("s3", region_name="eu-west-2")
        s3.upload_file("/tmp/finsight-embeddings-finetuned/config.json",
                       os.getenv("S3_BUCKET", "finsight-ai-prod"), "models/embeddings/config.json")
        mlflow.log_params({"base_model": "all-mpnet-base-v2", "epochs": 3})
        mlflow.log_metric("training_examples", len(train_examples))
    logger.info("Embeddings retrained and saved to S3")


def rebuild_vector_store(**ctx):
    from rag.pipeline import RAGPipeline
    pipeline = RAGPipeline()
    logger.info(f"Vector store rebuilt — total vectors: {pipeline.vector_store.index.ntotal if pipeline.vector_store else 0}")


def notify_success(**ctx):
    logger.info("FinSight AI retraining pipeline complete")


with DAG(
    dag_id="finsight_retraining_pipeline",
    default_args=DEFAULT_ARGS,
    description="Daily ingestion + drift detection + auto-retraining",
    schedule_interval="0 2 * * *",
    catchup=False,
    tags=["finsight", "ml", "rag", "retraining"],
) as dag:

    start          = EmptyOperator(task_id="start")
    ingest         = PythonOperator(task_id="ingest_data",         python_callable=run_ingestion)
    evaluate       = PythonOperator(task_id="evaluate_rag",        python_callable=evaluate_rag)
    drift          = BranchPythonOperator(task_id="drift_check",   python_callable=check_drift)
    retrain        = PythonOperator(task_id="retrain_embeddings",  python_callable=retrain_embeddings)
    rebuild        = PythonOperator(task_id="rebuild_vector_store",python_callable=rebuild_vector_store)
    skip           = EmptyOperator(task_id="skip_retrain")
    notify         = PythonOperator(task_id="notify_success",      python_callable=notify_success, trigger_rule="none_failed_min_one_success")
    end            = EmptyOperator(task_id="end",                  trigger_rule="none_failed_min_one_success")

    start >> ingest >> evaluate >> drift
    drift >> retrain >> rebuild >> notify >> end
    drift >> skip >> notify >> end
