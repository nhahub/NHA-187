
# import sys
# import os
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json, col
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# # ==================================================
# # 🧱 1️⃣ Schema Definition
# # ==================================================
# schema = StructType([
#     StructField("complaint_id", StringType(), True),
#     StructField("name", StringType(), True),
#     StructField("national_id", StringType(), True),
#     StructField("complaint", StringType(), True),
#     StructField("submitted_at", StringType(), True)
# ])

# # ==================================================
# # 🚀 2️⃣ Spark Session
# # ==================================================
# spark = SparkSession.builder \
#     .appName("SmartComplaintProcessor") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.33") \
#     .getOrCreate()

# spark.sparkContext.setLogLevel("WARN")
# print("✅ Spark session started successfully inside Docker!")

# # ==================================================
# # 📨 3️⃣ Read from Kafka
# # ==================================================
# # Note: In Docker, we use the service name 'kafka', not localhost
# kafka_df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("subscribe", "smart-complaints") \
#     .option("startingOffsets", "latest") \
#     .load()

# # Parse JSON
# json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
#     .select(from_json(col("json_str"), schema).alias("data")) \
#     .select("data.*")

# # ==================================================
# # 🧠 4️⃣ AI Processing (The Heavy Lifting)
# # ==================================================

# def process_partition(iterator):
#     """
#     This function runs on the Spark Worker.
#     It loads the models ONCE per batch, then processes all rows.
#     """
#     import torch
#     import joblib
#     import numpy as np
#     from transformers import AutoTokenizer, AutoModelForSequenceClassification
    
#     # --- PATHS INSIDE DOCKER CONTAINER ---
#     base_path = "/opt/spark/work-dir/processor/models"
#     path_tokenizer = f"{base_path}/tokenizer"
#     path_category = f"{base_path}/category_model"
#     path_sentiment = f"{base_path}/sentiment_model"
#     path_encoder = f"{base_path}/mlb_encoder.joblib"

#     # 1. Check if partition has data (Optimization)
#     rows = list(iterator)
#     if not rows:
#         return []

#     try:
#         # 2. LOAD MODELS (Only happens once per partition)
#         tokenizer = AutoTokenizer.from_pretrained(path_tokenizer)
        
#         # Load Safetensors Models
#         cat_model = AutoModelForSequenceClassification.from_pretrained(path_category, use_safetensors=True)
#         sent_model = AutoModelForSequenceClassification.from_pretrained(path_sentiment, use_safetensors=True)
        
#         # Load Scikit-Learn Encoder
#         encoder = joblib.load(path_encoder)

#         results = []

#         for row in rows:
#             text = row.complaint
#             if text:
#                 # A. Tokenize
#                 inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)

#                 # B. Predict Category
#                 with torch.no_grad():
#                     cat_outputs = cat_model(**inputs)
#                 cat_idx = torch.argmax(cat_outputs.logits, dim=-1).item()
                
#                 # Attempt to decode category name using the joblib encoder
#                 # Assuming it is a LabelEncoder or MultiLabelBinarizer
#                 try:
#                     if hasattr(encoder, 'classes_'):
#                         category_pred = encoder.classes_[cat_idx]
#                     else:
#                         category_pred = str(cat_idx)
#                 except:
#                     category_pred = str(cat_idx)

#                 # C. Predict Sentiment
#                 with torch.no_grad():
#                     sent_outputs = sent_model(**inputs)
#                 sent_idx = torch.argmax(sent_outputs.logits, dim=-1).item()
                
#                 # Simple mapping (Adjust based on your training labels 0,1,2)
#                 sentiment_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
#                 sentiment_pred = sentiment_map.get(sent_idx, "Unknown")

#                 # Append Result (Original Row + Predictions)
#                 results.append((
#                     row.complaint_id, 
#                     row.name, 
#                     row.national_id, 
#                     row.complaint, 
#                     row.submitted_at, 
#                     str(category_pred), 
#                     str(sentiment_pred)
#                 ))
        
#         return results

#     except Exception as e:
#         # If model loading fails, return error in fields
#         return [(row.complaint_id, row.name, row.national_id, row.complaint, row.submitted_at, "Error", str(e)) for row in rows]

# # ==================================================
# # 🗄️ 5️⃣ Write to MySQL
# # ==================================================

# def write_to_mysql(batch_df, batch_id):
#     if batch_df.count() == 0:
#         return

#     # 1. Run the AI Models using mapPartitions
#     rdd = batch_df.rdd.mapPartitions(process_partition)
    
#     if rdd.isEmpty():
#         return

#     # 2. Convert back to DataFrame
#     final_df = rdd.toDF([
#         "complaint_id", "name", "national_id", "complaint", "submitted_at", "category_prediction", "sentiment_prediction"
#     ])

#     # 3. Show in Console (Debug)
#     print(f"--- Batch {batch_id} Processed ---")
#     final_df.select("complaint", "category_prediction", "sentiment_prediction").show(truncate=False)

#     # 4. Write to MySQL
#     # IMPORTANT: In Docker, 'localhost' or '192.168.x.x' can be tricky.
#     # If using a MySQL Container, use "jdbc:mysql://mysql-container:3306/..."
#     print(f"💾 Writing batch {batch_id} to MySQL ...")
#     try:
#         final_df.write \
#             .format("jdbc") \
#             .mode("append") \
#             .option("url", "jdbc:mysql://mysql:3306/smart_complaints") \
#             .option("driver", "com.mysql.cj.jdbc.Driver") \
#             .option("dbtable", "complaints_analyzed") \
#             .option("user", "root") \
#             .option("password", "123123rm") \
#             .save()
#         print(f"✅ Batch {batch_id} written successfully.")
#     except Exception as e:
#         print(f"❌ Error writing to MySQL: {e}")

# # ==================================================
# # ⚡️ 6️⃣ Start Stream
# # ==================================================
# query = json_df.writeStream \
#     .foreachBatch(write_to_mysql) \
#     .start()

# print("🚀 Streaming started! Waiting for data...")
# query.awaitTermination()



from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import os
import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

# ==================================================
# 🧱 1️⃣ Define Input Schema
# ==================================================
schema = StructType([
    StructField("complaint_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("national_id", StringType(), True),
    StructField("complaint", StringType(), True),
    StructField("submitted_at", StringType(), True)
])

# ==================================================
# 🚀 2️⃣ Create Spark Session (FIXED)
# ==================================================
# Added the required JAR packages configuration
spark = SparkSession.builder \
    .appName("SmartComplaintProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,mysql:mysql-connector-java:8.0.33") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("✅ Spark session started successfully!")

# ==================================================
# 🧠 3️⃣ Model Paths
# ==================================================
# Ensure these paths match your Docker Volume Mount (/opt/spark/work-dir/processor/models...)
# Using absolute paths is safer in Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORY_MODEL_PATH = os.path.join(BASE_DIR, "models/category_model")
SENTIMENT_MODEL_PATH = os.path.join(BASE_DIR, "models/sentiment_model")
CATEGORY_LABELS_PATH = os.path.join(CATEGORY_MODEL_PATH, "mlb_classes.json")

# ... (Labels loading logic remains the same) ...
try:
    # Mocking labels if file not found to prevent crash during test
    if os.path.exists(CATEGORY_LABELS_PATH):
        with open(CATEGORY_LABELS_PATH, "r", encoding="utf-8") as f:
            CATEGORY_LABELS = json.load(f)
    else:
        CATEGORY_LABELS = ["Label_1", "Label_2"] # Fallback
except Exception as e:
    print(f"❌ ERROR: Failed to load CATEGORY_LABELS. {e}")
    CATEGORY_LABELS = []

# ==================================================
# 📝 4️⃣ UDF Definitions
# ==================================================
# Note: UDFs are slower than mapPartitions, but this logic is syntactically correct.
def classify_category_text(complaint_text: str) -> str:
    if not complaint_text: return "Unknown"
    
    # Global/Static loading trick to avoid reloading per row
    if not hasattr(classify_category_text, "model"):
        # Use 'safetensors=True' if your models are .safetensors
        classify_category_text.tokenizer = AutoTokenizer.from_pretrained(CATEGORY_MODEL_PATH)
        classify_category_text.model = AutoModelForSequenceClassification.from_pretrained(CATEGORY_MODEL_PATH)
    
    try:
        inputs = classify_category_text.tokenizer(complaint_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            logits = classify_category_text.model(**inputs).logits
        
        probs = torch.sigmoid(logits).numpy().flatten()
        pred_idx = np.argmax(probs)
        # Safety check for index
        if CATEGORY_LABELS and pred_idx < len(CATEGORY_LABELS):
            return CATEGORY_LABELS[pred_idx]
        return str(pred_idx)
    except Exception:
        return "Error"

def classify_sentiment_text(complaint_text: str) -> float:
    if not complaint_text: return 1.0
    
    if not hasattr(classify_sentiment_text, "model"):
        classify_sentiment_text.tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
        classify_sentiment_text.model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_PATH)

    try:
        inputs = classify_sentiment_text.tokenizer(complaint_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            logits = classify_sentiment_text.model(**inputs).logits
        
        # Assuming simple 3-class sentiment (0:Neg, 1:Neu, 2:Pos) mapped to Severity
        pred_idx = torch.argmax(logits, dim=-1).item()
        
        # Map Prediction to Severity (1=Low, 5=High)
        if pred_idx == 0: return 5.0 # Negative -> High Severity
        if pred_idx == 1: return 3.0 # Neutral
        return 1.0 # Positive -> Low Severity
    except Exception:
        return 1.0

category_udf = udf(classify_category_text, StringType())
sentiment_udf = udf(classify_sentiment_text, FloatType())

# ==================================================
# 📨 5️⃣ Read Stream (FIXED)
# ==================================================
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "smart-complaints") \
    .option("startingOffsets", "latest") \
    .load()

# ... (Processing logic remains same) ...
parsed_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

processed_df = parsed_df.withColumn("category_prediction", category_udf(col("complaint"))) \
                        .withColumn("sentiment_prediction", sentiment_udf(col("complaint")))

final_df = processed_df.select(
    col("complaint_id"), col("name"), col("national_id"), col("complaint"), 
    col("submitted_at"), col("category_prediction"), col("sentiment_prediction")
)

# ==================================================
# 🗄️ 7️⃣ JDBC Configuration (FIXED)
# ==================================================
# Use 'mysql' service name instead of IP to be safe in Docker
JDBC_URL = "jdbc:mysql://mysql:3306/smart_complaints" # <--- CHANGED IP to service name
TABLE_NAME = "complaints_analyzed" # Changed to match your init.sql table
MYSQL_USER = "root"
MYSQL_PASSWORD = "ةشغسشسشةغ123"

def write_to_mysql(df, epoch_id):
    if df.count() == 0: return
    print(f"[{epoch_id}] Writing data to MySQL...")
    try:
        df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", TABLE_NAME) \
            .option("user", MYSQL_USER) \
            .option("password", MYSQL_PASSWORD) \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .mode("append") \
            .save()
        print(f"✅ Batch {epoch_id} success!")
    except Exception as e:
        print(f"❌ Batch {epoch_id} failed: {e}")

# ==================================================
# ⚡️ 8️⃣ Start Stream
# ==================================================
query = final_df.writeStream \
    .foreachBatch(write_to_mysql) \
    .start()

query.awaitTermination()