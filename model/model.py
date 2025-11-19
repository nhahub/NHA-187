"""
LOCAL TRAINING VERSION – AraBERT sentiment regression + multi-label classification
VSCode + venv + Laptop GPU (NVIDIA) + CUDA
"""

import os, random
import numpy as np
import pandas as pd
from ast import literal_eval

import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, mean_squared_error, mean_absolute_error
import joblib

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    set_seed
)

# =========================
# 0) CONFIG
# =========================
CSV_PATH = "complaints_dataset_1000.csv"   # Place CSV here
MODEL_NAME = "aubmindlab/bert-base-arabertv2"
MAX_LEN = 64
RANDOM_SEED = 42
MODEL_SAVE_DIR = "./saved_model"
os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

# =========================
# 1) SEED
# =========================
set_seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# =========================
# 2) LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} rows from {CSV_PATH}")

expected_cols = ['id', 'text', 'categories', 'sentiment']
for c in expected_cols:
    if c not in df.columns:
        raise ValueError(f"Missing column: {c}")

def parse_categories(x):
    if isinstance(x, list): return x
    if pd.isna(x): return []
    try:
        v = literal_eval(x)
        if isinstance(v, (list, tuple)): return list(v)
        return [str(v)]
    except:
        return [str(x)] if x else []

df["categories"] = df["categories"].apply(parse_categories)
df["sentiment"] = pd.to_numeric(df["sentiment"], errors="coerce").fillna(0.0)

# =========================
# 3) ENCODE MULTI-LABEL TARGETS
# =========================
mlb = MultiLabelBinarizer()
y_categories = mlb.fit_transform(df['categories'])
y_sentiment = df["sentiment"].values.astype(np.float32)

train_idx, test_idx = train_test_split(
    range(len(df)), test_size=0.2, random_state=RANDOM_SEED, shuffle=True
)

train_df = df.iloc[train_idx].reset_index(drop=True)
test_df  = df.iloc[test_idx].reset_index(drop=True)
ycat_train = y_categories[train_idx]
ycat_test  = y_categories[test_idx]
ysent_train = y_sentiment[train_idx]
ysent_test  = y_sentiment[test_idx]

print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")

# =========================
# 4) TOKENIZER
# =========================
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# =========================
# 5) DATASETS
# =========================
class SentRegressionDataset(Dataset):
    def __init__(self, texts, targets):
        enc = tokenizer(list(texts), truncation=True, padding="max_length", max_length=MAX_LEN)
        self.enc = enc
        self.targets = list(targets)

    def __len__(self): return len(self.targets)

    def __getitem__(self, idx):
        item = {
            "input_ids": torch.tensor(self.enc["input_ids"][idx], dtype=torch.long),
            "attention_mask": torch.tensor(self.enc["attention_mask"][idx], dtype=torch.long),
            "labels": torch.tensor(self.targets[idx], dtype=torch.float)
        }
        return item

class MultiLabelDataset(Dataset):
    def __init__(self, texts, labels):
        enc = tokenizer(list(texts), truncation=True, padding="max_length", max_length=MAX_LEN)
        self.enc = enc
        self.labels = labels.astype(np.float32)

    def __len__(self): return len(self.labels)

    def __getitem__(self, idx):
        item = {
            "input_ids": torch.tensor(self.enc["input_ids"][idx], dtype=torch.long),
            "attention_mask": torch.tensor(self.enc["attention_mask"][idx], dtype=torch.long),
            "labels": torch.tensor(self.labels[idx], dtype=torch.float)
        }
        return item

sent_train_ds = SentRegressionDataset(train_df["text"], ysent_train)
sent_test_ds  = SentRegressionDataset(test_df["text"], ysent_test)
cat_train_ds  = MultiLabelDataset(train_df["text"], ycat_train)
cat_test_ds   = MultiLabelDataset(test_df["text"], ycat_test)

# =========================
# 6) MODELS
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

sent_model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=1, problem_type="regression"
).to(device)

cat_model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=y_categories.shape[1], problem_type="multi_label_classification"
).to("cpu")

# =========================
# 7) METRICS
# =========================
def compute_reg_metrics(p):
    preds = np.squeeze(p.predictions)
    labels = p.label_ids
    return {"mse": mean_squared_error(labels, preds),
            "mae": mean_absolute_error(labels, preds)}

def compute_cat_metrics(p):
    logits = p.predictions
    labels = p.label_ids
    preds = (torch.sigmoid(torch.tensor(logits)) > 0.5).int().numpy()
    f1 = f1_score(labels, preds, average="micro", zero_division=0)
    return {"f1_micro": f1}

# =========================
# 8) TRAINING ARGUMENTS
# =========================
common_args = dict(
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=2,
    load_best_model_at_end=True,
    fp16=False,
    logging_steps=20,
    weight_decay=0.01,
    warmup_ratio=0.06,
    report_to="none",
    seed=RANDOM_SEED
)

# Sentiment model
sent_args = TrainingArguments(
    output_dir="./sent_results",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=2,
    logging_steps=20,
    fp16=False,
    weight_decay=0.01,
    warmup_ratio=0.06,
    report_to="none",
    seed=RANDOM_SEED
)

cat_args = TrainingArguments(
    output_dir="./cat_results",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=2,
    logging_steps=20,
    fp16=False,
    weight_decay=0.01,
    warmup_ratio=0.06,
    report_to="none",
    seed=RANDOM_SEED,
)

# =========================
# 9) TRAINERS
# =========================
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

sent_trainer = Trainer(
    model=sent_model,
    args=sent_args,
    train_dataset=sent_train_ds,
    eval_dataset=sent_test_ds,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_reg_metrics
)

cat_trainer = Trainer(
    model=cat_model,
    args=cat_args,
    train_dataset=cat_train_ds,
    eval_dataset=cat_test_ds,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_cat_metrics
)
# =========================
# 10) TRAINING
# =========================
print("\nTraining sentiment model...")
sent_trainer.train()
print("\nSentiment evaluation:", sent_trainer.evaluate())

print("Saving sentiment model and tokenizer...")
sent_trainer.save_model(os.path.join(MODEL_SAVE_DIR, "sentiment_model"))
tokenizer.save_pretrained(os.path.join(MODEL_SAVE_DIR, "tokenizer"))

del sent_model
del sent_trainer
torch.cuda.empty_cache()
print("\nTraining multi-label model...")
cat_trainer.train()
print("\nCategory evaluation:", cat_trainer.evaluate())

print("Saving multi-label model and encoder...")
cat_trainer.save_model(os.path.join(MODEL_SAVE_DIR, "category_model"))
joblib.dump(mlb, os.path.join(MODEL_SAVE_DIR, "mlb_encoder.joblib"))
import json

with open(os.path.join(MODEL_SAVE_DIR, "category_model", "mlb_classes.json"), "w", encoding="utf-8") as f:
    json.dump(mlb.classes_.tolist(), f, ensure_ascii=False, indent=4)

# Free CPU memory if needed
del cat_model
del cat_trainer
torch.cuda.empty_cache()  # mostly for safety

# =========================
# 11) SAVE MODELS & ENCODERS
# =========================
#print("\nSaving models and tokenizer...")
#sent_trainer.save_model(os.path.join(MODEL_SAVE_DIR, "sentiment_model"))
#cat_trainer.save_model(os.path.join(MODEL_SAVE_DIR, "category_model"))
#tokenizer.save_pretrained(os.path.join(MODEL_SAVE_DIR, "tokenizer"))
#joblib.dump(mlb, os.path.join(MODEL_SAVE_DIR, "mlb_encoder.joblib"))

print("\n✅ All models and encoders saved successfully!")
