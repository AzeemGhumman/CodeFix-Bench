import os
import json
import pdb
import random


def select_random_files(repo_folder):
    file_extensions = (".py", ".js", ".java", ".cpp", ".h", ".cs")
    selected_files = []
    for root, _, files in os.walk(repo_folder):
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

            if not file.endswith(file_extensions):
                continue

            relative_path = os.path.relpath(file_path, repo_folder)
            selected_files.append(relative_path)

    total_items = min(len(selected_files), 20)
    return random.sample(selected_files, total_items)


# Load the JSON file
with open("../artifacts/entries.json", "r") as file:
    data = json.load(file)

db = {}
for idx, entry in enumerate(data):
    commit_hash = entry.get("base")
    repo_folder = f"../artifacts/repos/{commit_hash}"
    query = f"{entry.get('problem', '')} {entry.get('hint', '')}"

    print(repo_folder)

    results = select_random_files(repo_folder)

    db[entry.get("pr")] = {"results": [{"file": result} for result in results]}

with open("../artifacts/random.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
