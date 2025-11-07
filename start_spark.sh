#!/bin/bash

# ضبط متغيرات البيئة
export SPARK_HOME=~/SmartComplaintLocal/spark-3.5.7-bin-hadoop3
export PATH=$SPARK_HOME/bin:$PATH

# تشغيل PySpark مع الـ JARs المطلوبة
pyspark --jars \
$SPARK_HOME/jars/spark-sql-kafka-0-10_2.12-3.5.7.jar,\
$SPARK_HOME/jars/kafka-clients-3.4.0.jar,\
$SPARK_HOME/jars/mysql-connector-java-8.0.30.jar