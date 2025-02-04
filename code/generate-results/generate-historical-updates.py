import subprocess
import json
import pdb
import os
from collections import Counter

# Load the JSON file
with open("../artifacts/entries.json", "r") as file:
    data = json.load(file)

file_extensions = [".py", ".js", ".java", ".cpp", ".h", ".cs"]

db = {}
for idx, entry in enumerate(data):
    pr = entry.get("pr")
    commit_hash = entry.get("base")
    pr_parts = pr.split("/")
    repo_name = f"{pr_parts[0]}/{pr_parts[1]}"
    repo_url = f"https://github.com/{repo_name}.git"
    repo_folder = f"../artifacts/repos/{commit_hash}"

    print(repo_folder)

    # Run the git log command
    log = subprocess.check_output(
        ["git", "log", "--name-only", "--pretty=format:%H"], cwd=repo_folder, text=True
    )

    # Split log by commit hash
    commits = log.strip().split("\n\n")

    files_changed = []
    # Parse each commit and files
    for commit in commits:
        lines = commit.strip().split("\n")

        # commit_hash = lines[0]
        # files_changed = lines[1:]

        for file in lines[1:]:
            file_path = os.path.join(repo_folder, file)

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
                files_changed.append(file)

        files_changed += lines[1:]

        # print(f"Commit: {commit_hash}")
        # for file in files_changed:
        #     print(f"  - {file}")
        # print()  # Blank line between commits

    db[entry.get("pr")] = {
        "results": [
            {"file": filename, "changes": count}
            for filename, count in Counter(files_changed).most_common()
        ]
    }

with open("../artifacts/historical-frequency.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
