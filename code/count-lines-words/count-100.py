import json
import csv
import os
import pdb

# Directory containing the JSON files
json_dir = "/Users/azeem/workspace/code/personal/swe-paper-2024/final/intermediate/tasks"
csv_file = "lines.csv"
output_file = "lines-100.csv"

# Step 1: Extract all IDs from JSON files
json_ids = set()

for i in range(1, 101):
    json_path = os.path.join(json_dir, f"{i}.json")
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
            if "base" in data:
                json_ids.add(data["base"])

pdb.set_trace()

# Step 2: Filter rows from the CSV
filtered_rows = []

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] in json_ids:  # Check if ID is found in JSON IDs
            filtered_rows.append(row)

# Step 3: Save filtered rows to a new CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(filtered_rows)

print(f"Filtered rows saved to {output_file}")
