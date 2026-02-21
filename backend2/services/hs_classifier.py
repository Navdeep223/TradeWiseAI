import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from functools import lru_cache
from typing import List, Dict

MODEL_NAME = "all-MiniLM-L6-v2"
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data", "processed",
    "hs6_classification_clean.csv"
)
TOP_K = 3

@lru_cache(maxsize=1)
def _load_model():
    print(f"[HS Classifier] Loading model...")
    return SentenceTransformer(MODEL_NAME)

@lru_cache(maxsize=1)
def _load_data():
    path = os.path.abspath(DATA_PATH)
    print(f"[HS Classifier] Loading CSV from: {path}")
    df = pd.read_csv(path, dtype={"HS6": str})
    model = _load_model()
    print(f"[HS Classifier] Encoding {len(df)} descriptions...")
    embeddings = model.encode(
        df["HS_Description"].tolist(),
        batch_size=128,
        show_progress_bar=True,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    print("[HS Classifier] Ready.")
    return df, embeddings

def classify_hs_code(product_description: str) -> List[Dict]:
    model = _load_model()
    df, hs_embeddings = _load_data()
    query_emb = model.encode(
        product_description.strip(),
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    scores = util.dot_score(query_emb, hs_embeddings)[0].cpu().numpy()
    top_indices = np.argsort(scores)[::-1][:TOP_K]
    results = []
    for rank, idx in enumerate(top_indices, start=1):
        confidence = float(scores[idx])
        results.append({
            "rank": rank,
            "hs_code": str(df.iloc[idx]["HS6"]),
            "hs_description": str(df.iloc[idx]["HS_Description"]),
            "confidence": round(confidence, 4),
            "confidence_pct": f"{confidence * 100:.1f}%",
        })
    return results