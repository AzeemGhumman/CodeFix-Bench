import os
import json
import pdb
import random


def count_non_hidden_files_recursive(directory_path):
    total_files = 0
    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(directory_path):
        # Filter and count non-hidden files in the current directory
        non_hidden_files = [f for f in files if not f.startswith('.')]
        total_files += len(non_hidden_files)
    return total_files


# Load the JSON file
with open("../artifacts/entries.json", "r") as file:
    data = json.load(file)

db = {}
for idx, entry in enumerate(data):
    commit_hash = entry.get("base")
    repo_folder = f"../artifacts/repos/{commit_hash}"
    query = f"{entry.get('problem', '')} {entry.get('hint', '')}"
    files = entry.get("files")
    total_files_in_repo = count_non_hidden_files_recursive(repo_folder)

    print(repo_folder)

    db[entry.get("pr")] = {
        "issue_length": len(query.split()),
        "codebase_files": total_files_in_repo,
        "files_changed": len(files),
    }

with open("../artifacts/meta.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
