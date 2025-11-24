# Update to 2.10.2 (Supports Python 3.12)
FROM apache/airflow:2.10.2

USER root
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc && apt-get clean

USER airflow
RUN pip install apache-airflow-providers-mysql pandas openpyxl