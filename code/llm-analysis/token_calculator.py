import tiktoken
import os
import pdb


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# filepath = "../artifacts/blobs/9d69811e539774f296c2f289839147e741251716.txt"

# with open(filepath, "r") as file:
#     file_contents = file.read()

# tokens = num_tokens_from_string(file_contents, "o200k_base")
# print(tokens)




summaries_dir = "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts/llm"


# Iterate through each folder in the repo directory
for folder in os.listdir(summaries_dir):
    filepath = os.path.join(summaries_dir, folder)
    with open(filepath, "r") as file:
        file_contents = file.read()
    print (num_tokens_from_string(file_contents, "o200k_base"))