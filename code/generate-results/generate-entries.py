import pandas as pd
import pdb
import json

# Read the Parquet file into a DataFrame
df1 = pd.read_parquet("../SWE-bench/data/dev-00000-of-00001.parquet")
df2 = pd.read_parquet("../SWE-bench/data/test-00000-of-00001.parquet")
df3 = pd.read_parquet("../SWE-bench/data/train-00000-of-00001.parquet")

def get_modified_files(diff_string):
    modified_files = []
    for line in diff_string.split('\n'):
        if line.startswith('diff --git'):
            # Extract the file path after 'b/'
            file_path = line.split(' b/')[-1]
            modified_files.append(file_path)
    return modified_files

def get_item(row):
    return {
            "pr": f"{row["repo"]}/{row["instance_id"].split("-")[-1]}",
            "problem": row["problem_statement"],
            "hint": row["hints_text"],
            # "patch": row["patch"],
            "base": row["base_commit"],
            "env": row["environment_setup_commit"],
            "files": get_modified_files(row["patch"])
        }

items = []
for index, row in df1.iterrows():
    items.append(get_item(row))

with open("../artifacts/entries.json", "w") as json_file:
    json.dump(items, json_file, indent=4)
