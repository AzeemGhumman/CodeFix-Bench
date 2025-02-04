import json
import random
import pdb


def select_random_items(json_file, num_items):
    # Hard-coded seed
    seed = 42
    # Set the random seed for reproducibility
    random.seed(seed)

    # Load data from the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Randomly select items
    selected_items = random.sample(data, num_items)

    return selected_items


# Example usage
if __name__ == "__main__":
    json_file = "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts/entries.json"
    selected_items = select_random_items(json_file, 100)
    
    for item in selected_items:
        print (item['pr'])