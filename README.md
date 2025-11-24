# Smart Complaint System 🚀

An end-to-end real-time data pipeline that classifies Arabic customer complaints using AI, built with Apache Spark, Kafka, and Docker.

## 🏗 Architecture
1.  **Source:** Streamlit UI (User inputs complaint).
2.  **Ingestion:** Apache Kafka (KRaft mode).
3.  **Processing:** Apache Spark (Structured Streaming) + PyTorch (Hugging Face Models).
4.  **Storage:** MySQL Database.
5.  **Orchestration:** Apache Airflow (Daily Reporting).

## 🛠 Tech Stack
* **Language:** Python 3.9 / 3.10
* **Containers:** Docker & Docker Compose
* **AI:** PyTorch, Transformers (Arabic BERT)
* **Big Data:** PySpark 3.5

## 🚀 How to Run
1.  Clone the repo.
2.  Download the AI models and place them in `processor/models/`.
3.  Run the system:
    ```bash
    sudo docker compose up -d
    ```
4.  Start the Spark Processor:
    ```bash
    sudo docker exec -it spark-master /opt/spark/bin/spark-submit \
      --conf "spark.jars.ivy=/tmp/.ivy" \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.33 \
      --master spark://spark-master:7077 \
      /opt/spark/work-dir/processor/consumer_spark.py
    ```
5.  Access the UI at `http://localhost:8501`.
