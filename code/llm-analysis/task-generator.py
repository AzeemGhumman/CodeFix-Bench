import tiktoken
import os
import sys
import json
import copy
import pdb

output_folder = (
    "/Users/azeem/workspace/code/personal/swe-paper-2024/final/intermediate/tasks"
)
max_tokens = 300000

llm_input_root = (
    "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts/llm"
)

entries_filepath = "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts/entries.json"


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Get entries
entries = {}
with open(entries_filepath, "r") as file:
    all_entries = json.load(file)


# filter entries
prs = []
with open(
    "/Users/azeem/workspace/code/personal/swe-paper-2024/llm/llm_trials.txt", "r"
) as file:
    for line in file:
        # Strip newline characters and print each line
        prs.append(line.strip())

selected_entries = []
for entry in all_entries:
    if entry["pr"] in prs:
        selected_entries.append(entry)

for entry in selected_entries:
    entries[entry["base"]] = {
        "pr": entry["pr"],
        "problem": entry["problem"],
        "hint": entry["hint"],
        "base": entry["base"],
    }

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

file_counter = 0

for entry in selected_entries:

    filepath = os.path.join(llm_input_root, f"{entry["base"]}.txt")
    # print(f"processing: {filepath}")

    with open(filepath, "r") as file:
        file_contents = file.read()

        lines = file_contents.strip().split("\n")
        current_tokens = 0
        current_lines = []

        sections = []

        for line in lines:

            tokens_current_line = num_tokens_from_string(line, "o200k_base")

            if current_tokens + tokens_current_line > max_tokens:
                sections.append(list(current_lines))
                current_tokens = 0
                current_lines = list([])

            current_tokens += tokens_current_line
            current_lines.append(line)

        if len(current_lines) > 0:
            sections.append(list(current_lines))

        print(f"File Counter: {file_counter}, Tokens: {current_tokens}")

    for section_idx, section in enumerate(sections):

        repo_hash = filepath.split("/")[-1].split(".")[0]
        if repo_hash in entries:

            job = copy.deepcopy(entries[repo_hash])
            job["section"] = section_idx
            job["files"] = section

            file_counter += 1

            with open(f"{output_folder}/{file_counter}.json", "w") as file:
                json.dump(job, file, indent=4)
