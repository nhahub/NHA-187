from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# -------------------------------
# تعريف هيكل البيانات (Schema)
# -------------------------------
schema = StructType([
    StructField("name", StringType(), True),
    StructField("complaint", StringType(), True)
])

# -------------------------------
# إنشاء Spark Session
# -------------------------------
spark = SparkSession.builder \
    .appName("KafkaToConsoleTest") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -------------------------------
# قراءة البيانات من Kafka
# -------------------------------
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
    .option("subscribe", "complaints_topic") \
    .option("startingOffsets", "latest") \
    .load()

# -------------------------------
# تحويل قيمة الرسالة من bytes إلى string وParse JSON
# -------------------------------
complaints_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# -------------------------------
# عرض البيانات في الـ Console
# -------------------------------
query = complaints_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
