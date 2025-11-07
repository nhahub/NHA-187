from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# ==================================================
# 🧱 1️⃣ تعريف هيكل البيانات (Schema)
# ==================================================
schema = StructType([
    StructField("name", StringType(), True),
    StructField("national_id", StringType(), True),
    StructField("complaint", StringType(), True),
    StructField("submitted_at", StringType(), True)
])

# ==================================================
# 🚀 2️⃣ إنشاء Spark Session
# ==================================================
spark = SparkSession.builder \
    .appName("SmartComplaintProcessor") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7,"
            "mysql:mysql-connector-java:8.0.33") \
    .config("spark.eventLog.enabled", "true") \
    .config("spark.eventLog.dir", "/tmp/spark-events") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("✅ Spark session started successfully!")

# ==================================================
# 📨 3️⃣ قراءة البيانات من Kafka
# ==================================================
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "smart-complaints") \
    .option("startingOffsets", "latest") \
    .load()

print("✅ Connected to Kafka topic: complaints_topic")

# ==================================================
# 🔍 4️⃣ تحويل الرسالة من JSON
# ==================================================
complaints_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# ==================================================
# 🧾 5️⃣ عرض البيانات في الكونسول (للتجربة)
# ==================================================
debug_query = complaints_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# ==================================================
# 🗄️ 6️⃣ كتابة البيانات في MySQL
# ==================================================
def write_to_mysql(df, epoch_id):
    if df.count() == 0:
        print(f"⚠️ Batch {epoch_id} is empty — skipping write.")
        return

    print(f"💾 Writing batch {epoch_id} to MySQL ...")

    df.write \
        .format("jdbc") \
        .mode("append") \
        .option("url", "jdbc:mysql://192.168.1.2:3306/smart_complaints") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "complaints") \
        .option("user", "root") \
        .option("password", "ةشغسشسشةغ123") \
        .save()
    
    print(f"✅ Batch {epoch_id} written successfully.")

# ==================================================
# ⚡️ 7️⃣ تشغيل Stream
# ==================================================
mysql_query = complaints_df.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("append") \
    .start()

print("🚀 Streaming started! Waiting for data from Kafka...")

mysql_query.awaitTermination()
