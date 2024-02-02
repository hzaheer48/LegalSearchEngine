# Legal Search Engine

Welcome to the Legal Search Engine project! This search engine is designed to facilitate the retrieval of legal judgments and orders from the Supreme Court of Pakistan. The project involves various tasks, including data collection, vocabulary generation, inverted index construction, interface development, ranking, evaluation, information presentation, and report writing.

## Project Overview

### [Task 1] Data Collection

The first task involved gathering a textual document collection of legal judgments/orders from the Supreme Court of Pakistan. The corpus consists of 1000 to 1500 judgments/orders categorized into 5 to 10 classes, such as Criminal Cases, Civil Appeals, Human Rights, Suo Moto, and Family Cases.

The categorization is presented in a plain text file, showcasing category names and brief descriptions of each order in the respective category.

### [Task 2] Vocabulary Generation

For the vocabulary generation, each document in the collection was processed. The vocabulary includes terms and their index numbers, as well as a plain text file for documents and their index numbers.

### [Task 3] Inverted Index Construction

An inverted index was generated to store TFIDF and BM25 term weightings. Four plain text files were created, consisting of inverted index data for raw term frequency, log frequency weighting, TFIDF weighting, and BM25 weighting.

### [Task 4] Interface and Queries Benchmark

A simple web interface was developed to search legal documents. The interface, resembling a Google page, allows users to input queries. The query collection benchmark includes ten queries, with five two-word queries and five three-term queries.

### [Task 5] Cosine Similarity and Ranking

The application now computes the similarity between each document and query and ranks them accordingly. Information retrieval is performed on 10 queries for both TFIDF and BM25 weights. The results are presented in plain text files.

### [Task 6] Evaluation

The search engine is evaluated using precision, recall, f-measure, average precision, and mean average precision. Two plain text files are provided for each query, showing the required information for both TFIDF and BM25 weights.

### [Task 7] Information Presentation

The top 10 documents, based on cosine similarity between query and documents, are presented as abstracts in the form of a list of snippets. A word cloud is displayed on the right side for each page, considering words from the corresponding top documents.

### [Task 8] Report Writing

A comprehensive draft of the assignment, detailing the methodology, results, and findings, is included in the report.

## Getting Started

To run the Legal Search Engine locally, follow these steps:

1. Clone the repository: `git clone https://github.com/hzaheer48/LegalSearchEngine.git`
2. Navigate to the project directory: `cd LegalSearchEngine`
3. Run the web interface: `web_interface.py`
