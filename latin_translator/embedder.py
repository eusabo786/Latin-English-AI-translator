from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def encode(text):
    return model.encode([text])[0]


def most_similar(query, candidates):
    """
    candidates: list of (word, latin, meaning)
    """
    query_vec = encode(query)

    best_score = -1
    best_item = None

    for item in candidates:
        text = f"{item[0]} {item[2]}"
        vec = encode(text)

        score = cosine_similarity([query_vec], [vec])[0][0]

        if score > best_score:
            best_score = score
            best_item = item

    return best_item, best_score