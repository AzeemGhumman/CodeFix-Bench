import os
import json
import pdb


with open("../artifacts/entries.json", "r") as file:
    all_entries = json.load(file)

with open("../artifacts/tf-idf.json", "r") as file:
    all_tf_idf = json.load(file)

with open("../artifacts/vsm-cos.json", "r") as file:
    all_vsm_cos = json.load(file)

with open("../artifacts/bm-25.json", "r") as file:
    all_bm_25 = json.load(file)

total_setup_time = 0.0
total_query_time = 0.0
total_memory = 0.0

for idx, entry in enumerate(all_entries):
    ground_truth = entry["files"]
    pr = entry["pr"]
    tf_idf = all_tf_idf[pr]
    vsm_cos = all_vsm_cos[pr]
    bm_25 = all_bm_25[pr]

    # TODO: Set the target benchmark here
    benchmark = bm_25

    total_setup_time += benchmark["setup_time"]
    total_query_time += benchmark["query_time"]
    total_memory += benchmark["memory"]

avg_setup_time = round(total_setup_time * 100.0 / len(all_entries), 2)
avg_query_time = round(total_query_time * 100.0 / len(all_entries), 2)
avg_memory = round(total_memory * 100.0 / len(all_entries), 2)

print(avg_setup_time)
print(avg_query_time)
print(avg_memory)