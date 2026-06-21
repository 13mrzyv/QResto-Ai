"""
RAG System - Finding similar examples using embeddings
"""

import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from examples import NUMUNELER_LIST as EXAMPLES

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Cache - calculated once when server starts
_example_vectors = None


def get_embedding(text: str):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def calculate_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def prepare_example_vectors():
    """Calculates embeddings for all examples and stores them in memory. Called once on server startup."""
    global _example_vectors
    print("Calculating example embeddings...")
    _example_vectors = []
    for example in EXAMPLES:
        vector = get_embedding(example["sual"])
        _example_vectors.append((vector, example))
    print(f"{len(EXAMPLES)} examples ready.")


def find_closest_examples(question: str, count: int = 3):
    """Finds the closest examples to the user's question (uses cache)."""
    if _example_vectors is None:
        prepare_example_vectors()

    question_vector = get_embedding(question)

    results = []
    for example_vector, example in _example_vectors:
        similarity = calculate_similarity(question_vector, example_vector)
        results.append((similarity, example))

    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:count]]