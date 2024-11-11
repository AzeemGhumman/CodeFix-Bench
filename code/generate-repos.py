import json
import pdb
from git import Repo
import os
import shutil


def clone_at_commit(repo_url, commit_hash, destination_path):
    print(f"Cloning repo {repo_url} at {commit_hash}")
    try:
        # Clone the repository
        repo = Repo.clone_from(repo_url, destination_path)

        # Checkout the specific commit
        repo.git.checkout(commit_hash)
        print(f"Successfully cloned repository")

    except Exception as e:
        print(f"Error: {str(e)}")
        pdb.set_trace()


# Load the JSON file
with open("../artifacts/entries.json", "r") as file:
    data = json.load(file)

skip = False
for entry in data:
    pr = entry.get("pr")
    commit_hash = entry.get("base")
    pr_parts = pr.split("/")
    repo_name = f"{pr_parts[0]}/{pr_parts[1]}"
    repo_url = f"https://github.com/{repo_name}.git"
    destination_path = f"../artifacts/repos/{commit_hash}"

    # if commit_hash == "b682e1dc71eda183786ad724da25f2fb30b5a621":
    #     skip = False

    if not skip:
        # Make sure destination directory doesn't exist
        if os.path.exists(destination_path):
            shutil.rmtree(destination_path)

        clone_at_commit(repo_url, commit_hash, destination_path)
