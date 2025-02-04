import os
import json
import pdb

artifacts_folder = "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts"


with open(f"{artifacts_folder}/entries.json", "r") as file:
    all_entries = json.load(file)

with open(f"{artifacts_folder}/meta.json", "r") as file:
    all_meta = json.load(file)

with open(f"{artifacts_folder}/bm25.json", "r") as file:
    all_bm_25 = json.load(file)


def is_top_k(ground_truth, attempt, k):
    test_files = [i["file"] for i in attempt["results"]][:k]
    for item in ground_truth:
        if item in test_files:
            return 1
    return 0


def compute_map_score(ground_truth, attempt):
    test_files = [i["file"] for i in attempt["results"]]
    total_precision = 0.0
    found_count = 0

    for i, gt_item in enumerate(ground_truth):
        if gt_item in test_files:
            index = test_files.index(gt_item)
            precision = (i + 1) / (index + 1)
            total_precision += precision
            found_count += 1.0

    return total_precision / len(ground_truth) if found_count > 0 else 0.0


issue_length_short = 0
issue_length_long = 0
issue_codebase_small = 0
issue_codebase_large = 0
issue_scope_single = 0
issue_scope_multiple = 0

issue_length_short_all = 0
issue_length_long_all = 0
issue_codebase_small_all = 0
issue_codebase_large_all = 0
issue_scope_single_all = 0
issue_scope_multiple_all = 0


metas = []

for idx, entry in enumerate(all_entries):
    ground_truth = entry["files"]
    pr = entry["pr"]
    
    if pr not in all_meta:
        continue
    
    if pr not in all_bm_25:
        continue
    
    meta = all_meta[pr]
    bm_25 = all_bm_25[pr]

    benchmark = bm_25
    # TODO: Set Top k
    k = 5

    if meta["issue_length"] < 250:
        issue_length_short_all += 1
    else:
        issue_length_long_all += 1
    if meta["codebase_files"] < 500:
        issue_codebase_small_all += 1
    else:
        issue_codebase_large_all += 1
    if meta["files_changed"] == 1:
        issue_scope_single_all += 1
    else:
        issue_scope_multiple_all += 1

    if is_top_k(ground_truth, benchmark, k):
        if meta["issue_length"] < 250:
            issue_length_short += 1
        else:
            issue_length_long += 1
        if meta["codebase_files"] < 500:
            issue_codebase_small += 1
        else:
            issue_codebase_large += 1
        if meta["files_changed"] == 1:
            issue_scope_single += 1
        else:
            issue_scope_multiple += 1

    # map_score = compute_map_score(ground_truth, benchmark)
    # if meta["issue_length"] < 250:
    #     issue_length_short += map_score
    # else:
    #     issue_length_long += map_score
    # if meta["codebase_files"] < 500:
    #     issue_codebase_small += map_score
    # else:
    #     issue_codebase_large += map_score
    # if meta["files_changed"] == 1:
    #     issue_scope_single += map_score
    # else:
    #     issue_scope_multiple += map_score


f_length_short = round(issue_length_short * 100.0 / issue_length_short_all, 2)
f_length_long = round(issue_length_long * 100.0 / issue_length_long_all, 2)
f_codebase_small = round(issue_codebase_small * 100.0 / issue_codebase_small_all, 2)
f_codebase_large = round(issue_codebase_large * 100.0 / issue_codebase_large_all, 2)
f_scope_single = round(issue_scope_single * 100.0 / issue_scope_single_all, 2)
f_scope_multiple = round(issue_scope_multiple * 100.0 / issue_scope_multiple_all, 2)

# f_length_short = round(issue_length_short / issue_length_short_all, 2)
# f_length_long = round(issue_length_long / issue_length_long_all, 2)
# f_codebase_small = round(issue_codebase_small / issue_codebase_small_all, 2)
# f_codebase_large = round(issue_codebase_large / issue_codebase_large_all, 2)
# f_scope_single = round(issue_scope_single / issue_scope_single_all, 2)
# f_scope_multiple = round(issue_scope_multiple / issue_scope_multiple_all, 2)


print(f_length_short)
print(f_length_long)
print(f_codebase_small)
print(f_codebase_large)
print(f_scope_single)
print(f_scope_multiple)
