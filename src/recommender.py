# src/recommender.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from difflib import SequenceMatcher
import re

# ---------- Load Data ----------
train_df = pd.read_excel("data/Gen_AI Dataset.xlsx", sheet_name="Train-Set")
test_df = pd.read_excel("data/Gen_AI Dataset.xlsx", sheet_name="Test-Set")

# Combine all unique assessment URLs from dataset
all_urls = pd.concat([train_df["Assessment_url"]]).unique().tolist()

# Function to extract readable names
def name_from_url(url):
    parts = [p for p in url.split("/") if p and p not in ["https:", "www.shl.com", "solutions", "products", "product-catalog", "view"]]
    if not parts:
        return "Unknown Assessment"
    name = re.sub(r"[-_]+", " ", parts[-1]).strip()
    name = re.sub(r"\d+", "", name)
    name = re.sub(r"\s+", " ", name)
    if len(name) < 2:
        name = "Unnamed Assessment"
    return name.title()

# Create a clean DataFrame for all assessments
catalog_df = pd.DataFrame({
    "url": all_urls,
    "name": [name_from_url(u) for u in all_urls]
})

# Deduplicate
catalog_df = catalog_df.drop_duplicates(subset="url")

# Create a 'text' column for embedding (name + partial url)
catalog_df["text"] = catalog_df["name"] + " " + catalog_df["url"]

# ---------- Model ----------
model = SentenceTransformer("all-MiniLM-L6-v2")
catalog_embeddings = model.encode(catalog_df["text"].tolist(), convert_to_numpy=True)

# ---------- Recommendation Function ----------
def recommend(query, top_k=10):
    q_emb = model.encode([query], convert_to_numpy=True)
    sims = cosine_similarity(q_emb, catalog_embeddings)[0]

    scored = []
    for i, row in catalog_df.iterrows():
        name_sim = SequenceMatcher(None, query.lower(), row["name"].lower()).ratio()
        final_score = 0.85 * sims[i] + 0.15 * name_sim
        scored.append((final_score, row["url"], row["name"]))
    scored.sort(reverse=True, key=lambda x: x[0])
    results = [{"assessment_name": n, "url": u, "score": float(s)} for s, u, n in scored[:top_k]]
    return results

# ---------- Generate submission CSV ----------
def generate_submission():
    rows = []
    for q in test_df["Query"]:
        recs = recommend(q, top_k=10)
        for r in recs:
            rows.append([q, r["url"]])
    out = pd.DataFrame(rows, columns=["Query", "Assessment_url"])
    out.to_csv("predictions_submission.csv", index=False)
    print("✅ Saved predictions_submission.csv with", len(rows), "rows.")

if __name__ == "__main__":
    print("Testing recommender with full dataset:")
    print(recommend("Hiring an analyst skilled in problem solving and teamwork"))
