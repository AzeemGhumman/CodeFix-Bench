import os
import json
import pdb

artifacts_folder = (
    "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts"
)

with open(f"{artifacts_folder}/entries.json", "r") as file:
    all_entries = json.load(file)

with open(f"{artifacts_folder}/tf-idf.json", "r") as file:
    all_tf_idf = json.load(file)

with open(f"{artifacts_folder}/vsm-cos.json", "r") as file:
    all_vsm_cos = json.load(file)

with open(f"{artifacts_folder}/bm25.json", "r") as file:
    all_bm_25 = json.load(file)

total_setup_time = 0.0
total_query_time = 0.0
total_memory = 0.0

count_total = 0
for idx, entry in enumerate(all_entries):
    ground_truth = entry["files"]
    pr = entry["pr"]

    if pr not in all_bm_25:
        continue

    count_total += 1

    tf_idf = all_tf_idf[pr]
    vsm_cos = all_vsm_cos[pr]
    bm_25 = all_bm_25[pr]

    # TODO: Set the target benchmark here
    benchmark = bm_25

    total_setup_time += benchmark["setup_time"]
    total_query_time += benchmark["query_time"]
    total_memory += benchmark["memory"]

avg_setup_time = round(total_setup_time / count_total, 2)
avg_query_time = round(total_query_time / count_total, 2)
avg_memory = round(total_memory / count_total, 2)

print(avg_setup_time)
print(avg_query_time)
print(avg_memory)
