
# CodeScout-Bench

**CodeScout-Bench: A Large-Scale Benchmark for Mapping Issue Reports to Code Files**

## Overview

CodeScout-Bench is a comprehensive dataset and benchmark designed to support research in code localization. This benchmark aids models in identifying files relevant to a code fix based on plain-text inputs, such as bug reports and feature requests.

## Contents

- **Dataset**: Contains issue reports paired with corresponding files within a codebase that are likely to be impacted.
- **Retrieval Methods**: Includes tf-idf, VSM with cosine similarity, and BM25, along with historical and random baselines.
- **Evaluation**: Provides a framework for evaluating retrieval models in identifying relevant files from issue reports.

## Usage

1. **Preprocess Data**: Filter out non-code files, hidden files, and test directories.
2. **Construct Index**: Generate document-term matrices and similarity scores for tf-idf, VSM-cosine, and BM25 retrieval methods.
3. **Query and Rank**: Input an issue report to produce a ranked list of relevant files.

## Requirements

- Python 3.x
- NLTK
- Sci-kit Learn
- Other dependencies specified in `requirements.txt`

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/CodeScout-Bench.git
   cd CodeScout-Bench
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Contributing

Contributions are welcome! Please read the contributing guidelines and open an issue or pull request.
