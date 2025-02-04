import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pathlib import Path
from typing import List, Tuple
import re
import json
import pdb
import time
from pympler import asizeof


class RepoSearcher:
    def __init__(self, repo_path: str):
        """
        Initialize the VSM Code Search with a local repository path.

        Args:
            repo_path (str): Path to the local repository
        """
        self.repo_path = repo_path
        self.documents = {}  # Dictionary to store document contents
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            token_pattern=r"(?u)\b\w+\b",  # Matches single word tokens
            max_features=10000,  # Limit vocabulary size
            ngram_range=(1, 2),  # Include both unigrams and bigrams
        )
        self.tfidf_matrix = None

    def index_repository(
        self, file_extensions: List[str] = [".py", ".js", ".java", ".cpp", ".h", ".cs"]
    ):
        """
        Index all files in the repository with specified extensions.

        Args:
            file_extensions (List[str]): List of file extensions to index
        """
        documents = []
        file_paths = []

        # Walk through the repository
        for root, _, files in os.walk(self.repo_path):
            for file in files:

                file_path = os.path.join(root, file)

                # Skip hidden files
                if file.startswith("."):
                    continue
                # Ignore __init__.py format files
                if "__.py" in file:
                    continue
                # Ignore files in test directory
                if "/test/" in file_path:
                    continue

                if any(file.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            relative_path = os.path.relpath(file_path, self.repo_path)
                            documents.append(content)
                            file_paths.append(relative_path)
                            self.documents[relative_path] = content
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")

        if not documents:
            raise ValueError("No documents were found to index")

        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        self.file_paths = file_paths

    def search(self, query: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Search for relevant documents based on a query.

        Args:
            query (str): Search query
            top_k (int): Number of top results to return

        Returns:
            List[Tuple[str, float]]: List of (document_path, similarity_score) pairs
        """
        if self.tfidf_matrix is None:
            raise ValueError("Repository has not been indexed yet")

        # Transform query using the same vectorizer
        query_vector = self.vectorizer.transform([query])

        # Calculate cosine similarities
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Get top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        # Create results list
        results = [
            (self.file_paths[idx], float(similarities[idx]))
            for idx in top_indices
            if similarities[idx] > 0
        ]

        return results


# Load the JSON file
with open("../artifacts/entries.json", "r") as file:
    data = json.load(file)

db = {}
for idx, entry in enumerate(data):
    commit_hash = entry.get("base")
    repo_folder = f"../artifacts/repos/{commit_hash}"
    query = f"{entry.get('problem', '')} {entry.get('hint', '')}"

    print(repo_folder)

    # Initialize and use the searcher
    start_setup_time = time.time()
    searcher = RepoSearcher(repo_folder)
    searcher.index_repository()
    total_size = asizeof.asizeof(searcher)
    total_setup_time = round(float(time.time() - start_setup_time), 6)

    start_query_time = time.time()
    results = searcher.search(query)
    total_query_time = round(float(time.time() - start_query_time), 6)

    matches = []
    for file_path, score in results:
        matches.append({"file": file_path, "score": round(float(score), 3)})

    db[entry.get("pr")] = {
        "results": matches,
        "setup_time": total_setup_time,
        "query_time": total_query_time,
        "memory": total_size,
    }

with open("../artifacts/vsm-cos.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
