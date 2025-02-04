# Role Based
# Prompt 1
prompt = f"""
### ROLE
You are a senior software engineer specializing in debugging and maintaining large codebases. Your experience allows you to efficiently pinpoint files that require modification to resolve a given problem.

### Objectives
- Analyze the problem statement, optional hint, and list of files (with function details).
- Output the files in descending order of confidence score.

### Instructions
- Only return the name of the files, do not return anything else.
- Identify 20 files most relevant to resolving the problem.
- Assign a confidence score between 0 and 1 to each file, based on its likelihood of being involved in the issue.
- Output exactly 20 lines, each in the format: file_name, confidence_score
- Output the files in descending order of confidence score.
- Do not include explanations, comments, or extra text.

[PROBLEM_STATEMENT,]{job['problem']}[/PROBLEM_STATEMENT]
[HINT]{job['hint']}[/HINT]
[LIST_OF_FILES]{"\n".join(job['files'])}[/LIST_OF_FILES]

### Results
Here are 20 comma separated list of files with their confidence scores
[RESULT]
"""

# Task Based
# Prompt 2
prompt = f"""
### TASK
Your objective is to determine which files in a repository need modification to resolve a given issue.

### STEPS TO FOLLOW
- Analyze the problem statement, optional hint, and list of files (with function details).
- Select 20 files that are most likely to be affected.
- Assign a confidence score (between 0 and 1) for each file based on its relevance.
- Output the files in descending order of confidence score.

### INSTRUCTIONS
- Only return the name of the files, do not return anything else.
- Do not include explanations, comments, or extra text.
- Output exactly 20 lines, each in the format: file_name, confidence_score.

[PROBLEM_STATEMENT,]{job['problem']}[/PROBLEM_STATEMENT]
[HINT]{job['hint']}[/HINT]
[LIST_OF_FILES]{"\n".join(job['files'])}[/LIST_OF_FILES]

### RESULT
Here are 20 comma separated list of files with their confidence scores
[RESULT]
"""
