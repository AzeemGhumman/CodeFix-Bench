import os
import numpy as np
from pathlib import Path
import re
import json
import pdb
import time
from rank_bm25 import BM25Okapi
from typing import List, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from pympler import asizeof

# import nltk
# nltk.download('punkt')


class RepoSearcher:
    def __init__(self, repo_path: str):
        """
        Initialize the searcher with the path to the local repository

        Args:
            repo_path (str): Path to the local repository
        """
        self.repo_path = repo_path
        self.documents = []
        self.file_paths = []
        self.bm25 = None

        # Download required NLTK data
        try:
            nltk.data.find("tokenizers/punkt")
            nltk.data.find("corpora/stopwords")
        except LookupError:
            nltk.download("punkt")
            nltk.download("stopwords")

        self._load_documents()
        self._create_bm25_index()

    def _load_documents(self):
        """Load all text files from the repository"""
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
                if not file.endswith((".py", ".js", ".java", ".cpp", ".h", ".cs")):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self.documents.append(content)
                    self.file_paths.append(file_path)
                except (UnicodeDecodeError, IOError):
                    continue

    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess the text by tokenizing, removing stopwords and punctuation

        Args:
            text (str): Input text

        Returns:
            List[str]: List of preprocessed tokens
        """
        # Tokenize
        tokens = word_tokenize(text.lower())

        # Remove stopwords and punctuation
        stop_words = set(stopwords.words("english"))
        tokens = [
            token
            for token in tokens
            if token not in stop_words and token not in string.punctuation
        ]

        return tokens

    def _create_bm25_index(self):
        """Create BM25 index from the documents"""
        tokenized_documents = [self._preprocess_text(doc) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_documents)

    def get_relative_paths(self, full_paths):
        return [os.path.relpath(i, self.repo_path) for i in full_paths]

    def search(self, query: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Search for relevant documents based on the query

        Args:
            query (str): Search query
            top_k (int): Number of top results to return

        Returns:
            List[Tuple[str, float]]: List of (file_path, score) tuples
        """
        # Preprocess the query
        tokenized_query = self._preprocess_text(query)

        # Get document scores
        doc_scores = self.bm25.get_scores(tokenized_query)

        # Create (file_path, score) pairs and sort by score
        results = list(zip(self.get_relative_paths(self.file_paths), doc_scores))
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]


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

with open("../artifacts/bm-25.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
