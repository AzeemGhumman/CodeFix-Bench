import os
import ast
import pdb
import json


def annotate_parents(node, parent=None):
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        annotate_parents(child, node)


def extract_definitions(file_path):
    """
    Extract class names with their methods and standalone functions from a Python file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            tree = ast.parse(file.read())
        except SyntaxError:
            print(f"Could not parse {file_path}")
            return {}, []

    # By default, class method's parent is not class. This is why we need this helper method
    annotate_parents(tree)

    ast_items = []
    for node in ast.walk(tree):

        # Extract class definitions and their methods
        if isinstance(node, ast.ClassDef):
            methods = [
                f"{node.name}.{child.name}"
                for child in node.body
                if isinstance(child, ast.FunctionDef)
            ]
            ast_items += methods

        # Extract standalone functions (no parent or parent not a class)
        elif isinstance(node, ast.FunctionDef) and not isinstance(
            getattr(node, "parent", None), ast.ClassDef
        ):
            ast_items.append(node.name)

    return ast_items


def process_repository(repo_path):
    """
    Process all Python files in the repository to extract class methods and standalone functions.
    """
    results = {}
    for root, dirs, files in os.walk(repo_path):

        # Skip files in test folder
        if "/test" in root:
            continue

        for file in files:
            # Skip non-python files
            if not file.endswith(".py"):
                continue
            file_path = os.path.join(root, file)
            try:
                items = extract_definitions(file_path)
                if len(items) > 0:
                    filename = file_path[len(repo_path) + 1 :]
                    results[filename] = items
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return results


repo_dir = "../artifacts/repos"
summaries_dir = "../artifacts/summaries-text-2"

# Ensure the summaries directory exists
os.makedirs(summaries_dir, exist_ok=True)

# Iterate through each folder in the repo directory
for folder in os.listdir(repo_dir):
    folder_path = os.path.join(repo_dir, folder)
    # Check if it's a directory
    if os.path.isdir(folder_path):
        # json_filename = f"{folder}.json"
        json_filename = f"{folder}.txt"
        json_filepath = os.path.join(summaries_dir, json_filename)

        results = process_repository(folder_path)

        # with open(json_filepath, "w") as json_file:
        #     json.dump(results, json_file, indent=4)

        with open(json_filepath, "w") as json_file:
            for key, value in results.items():
                json_file.write(f"{key}:{','.join(value)}\n")

print("Done")
