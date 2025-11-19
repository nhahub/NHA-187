import torch
import numpy as np
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ================================
# Load sentiment model
# ================================
sent_tokenizer = AutoTokenizer.from_pretrained("./saved_model/sentiment_model")
sent_model = AutoModelForSequenceClassification.from_pretrained("./saved_model/sentiment_model")
sent_model.eval()

# ================================
# Load category model
# ================================
cat_tokenizer = AutoTokenizer.from_pretrained("./saved_model/category_model")
cat_model = AutoModelForSequenceClassification.from_pretrained("./saved_model/category_model")
cat_model.eval()

# ================================
# Load category labels
# ================================
with open("saved_model/category_model/mlb_classes.json", "r", encoding="utf-8") as f:
    classes = json.load(f)

# ================================
# Test samples
# ================================
TEST_SENTENCES = [
    "النت قطع",
    "الموظف كان محترم جدًا وخلصلي الموضوع بسرعة",
    "العيش ريحته وحشة ومش نضيف",
    "البطاقة بايظه",
    "السلع خلصانه"
]

print("\n=== RUNNING TEST CASES ===")

for text in TEST_SENTENCES:
    # --------- Sentiment ---------
    inputs = sent_tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        sent_logits = sent_model(**inputs).logits
    sentiment_score = float(sent_logits.squeeze().numpy())

    # --------- Categories ---------
    inputs = cat_tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        cat_logits = cat_model(**inputs).logits

    probs = torch.sigmoid(cat_logits).numpy().flatten()
    pred_bin = (probs > 0.5).astype(int)

    picked = [classes[i] for i, v in enumerate(pred_bin) if v == 1]
    if not picked:
        picked = [classes[int(np.argmax(probs))]]

    print("\nText:", text)
    print("→ Sentiment:", sentiment_score)
    print("→ Categories:", picked)
    print("→ Probabilities:", np.round(probs, 3))

print("\n=== TESTS DONE ===\n")
