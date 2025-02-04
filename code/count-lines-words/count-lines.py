import pdb
import os
import csv


def count_lines_and_words_in_folder(folder_path):
    total_lines = 0
    total_words = 0

    for root, _, files in os.walk(folder_path):
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

            # Skip unknown files extensions
            if not file.endswith((".py", ".js", ".java", ".cpp", ".h", ".cs")):
                continue

            try:
                # Open and count lines in the file
                with open(file_path, "r") as f:
                    for line in f:
                        total_lines += 1
                        total_words += len(line.split())
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return total_lines, total_words


def generate_folder_line_counts_csv(root_folder, output_csv):
    folder_line_counts = []

    # Iterate over each subfolder in the root folder
    for subfolder in sorted(os.listdir(root_folder)):
        subfolder_path = os.path.join(root_folder, subfolder)
        if os.path.isdir(subfolder_path):  # Ensure it's a directory
            total_lines, total_words = count_lines_and_words_in_folder(subfolder_path)
            folder_line_counts.append([subfolder, total_lines, total_words])

    # Write to CSV
    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Folder Name", "Total Lines"])
        writer.writerows(folder_line_counts)


if __name__ == "__main__":
    root_folder = "/Users/azeem/workspace/code/personal/swe-paper-2024/artifacts/repos"
    output_csv = "lines.csv"
    generate_folder_line_counts_csv(root_folder, output_csv)
    print(f"CSV file generated: {output_csv}")
