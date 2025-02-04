import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pathlib import Path
import re
import json
import pdb
import time
from pympler import asizeof


class RepoSearcher:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.documents = []
        self.file_paths = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = None

    def load_repository(
        self, file_extensions=(".py", ".js", ".java", ".cpp", ".h", ".cs")
    ):
        """
        Load all text files from the repository
        """
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

                # Skip unknown files extensions
                if file.endswith(file_extensions):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            self.documents.append(content)
                            self.file_paths.append(file_path)
                    except Exception as e:
                        print(f"Error reading file {file_path}: {str(e)}")

        # Create TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def search(self, query, top_k=20):
        """
        Search for relevant files based on the query
        """
        if self.tfidf_matrix is None:
            raise ValueError("Repository not loaded. Call load_repository() first.")

        # Transform query using the same vectorizer
        query_vector = self.vectorizer.transform([query])

        # Calculate similarity between query and all documents
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)

        # Get top k results
        top_indices = np.argsort(similarities[0])[::-1][:top_k]

        results = []
        for idx in top_indices:
            if (
                similarities[0][idx] > 0
            ):  # Only include results with non-zero similarity
                relative_path = os.path.relpath(self.file_paths[idx], self.repo_path)
                results.append(
                    {
                        "file": relative_path,
                        "similarity": similarities[0][idx],
                        "absolute_path": self.file_paths[idx],
                    }
                )

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
    searcher.load_repository()
    total_size = asizeof.asizeof(searcher)
    total_setup_time = round(float(time.time() - start_setup_time), 6)

    start_query_time = time.time()
    results = searcher.search(query)
    total_query_time = round(float(time.time() - start_query_time), 6)

    matches = []
    for result in results:
        matches.append(
            {"file": result["file"], "score": round(float(result["similarity"]), 3)}
        )
    db[entry.get("pr")] = {
        "results": matches,
        "setup_time": total_setup_time,
        "query_time": total_query_time,
        "memory": total_size,
    }

with open("../artifacts/tf-idf.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
