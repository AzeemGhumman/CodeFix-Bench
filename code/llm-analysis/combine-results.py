import os
import json
import pdb


def parse_results(text):
    start = "(content='"
    end = "', refusal=None"
    sub = text[text.find(start) + len(start) : text.find(end)]
    files = [i.strip().split(",")[0] for i in sub.split(" \\n")]
    return [{"file": f} for f in files]


def read_and_combine_json_files(folder_name, output_file):
    combined_data = {}

    # Iterate through all files in the folder
    for file_name in sorted(os.listdir(folder_name)):
        # Check for .json files only
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                files = parse_results(data["results"])
                combined_data[data["pr"]] = {"results": files}

    # Write the combined data to a single output JSON file
    with open(output_file, "w") as output_json:
        json.dump(combined_data, output_json, indent=4)


if __name__ == "__main__":
    folder_name = "../data/task/task_run_3/"
    output_file = "task-run-3.json"
    read_and_combine_json_files(folder_name, output_file)
