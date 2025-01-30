# Question-Answer Clustering with Sentence Transformers and KMeans

This project uses `SentenceTransformer` and `KMeans` clustering to match questions to their corresponding answers based on embeddings. It leverages MongoDB for storing question-answer pairs and FastAPI for managing the application state.

## Features

- **Question-Answer Clustering**: Uses sentence embeddings to cluster questions and associate them with predefined answers.
- **Efficient Question Matching**: When a question is asked, the model finds the nearest cluster and returns the most appropriate answer.
- **MongoDB Integration**: Loads question-answer data from a MongoDB database.
- **Async Model Preloading**: Uses FastAPI's async context manager to preload models and clustering on app startup.

## Requirements

- Python 3.8+
- Install required dependencies:
  ```bash
  pip install sentence-transformers scikit-learn scipy fastapi pymongo
  ```

## Setup

1. **MongoDB Setup**:
   - Ensure your MongoDB database contains collections with questions and their corresponding answers. 
   - The data should be loaded via the `load_data_from_mongo()` function (you may need to modify it to match your database schema).

2. **Start FastAPI Server**:
   - This project uses FastAPI to handle requests. You can start the FastAPI app with `uvicorn`:
   ```bash
   uvicorn main:app --reload
   ```

## Code Overview

### 1. **Loading Data from MongoDB**
The data is loaded through the `load_data_from_mongo()` function (assumed to be in the `db.py` file). It retrieves questions and their corresponding answers.

### 2. **Embedding Questions**
The `SentenceTransformer` model (`all-MiniLM-L6-v2`) is used to generate vector embeddings of the questions. These embeddings are then clustered using `KMeans`.

### 3. **KMeans Clustering**
KMeans is applied to group similar questions together. Each cluster corresponds to a set of questions that should map to the same answer. The cluster's centroid is used to identify the closest question in that cluster.

### 4. **Getting the Answer**
When a new question is provided to the `get_answer()` function, it is encoded into an embedding. The closest cluster is determined, and the corresponding answer is retrieved.

### 5. **Async Context Manager for Preloading**
The `preload_models()` async context manager loads the model and performs clustering when the FastAPI app starts up. It ensures the model and clustering are available for efficient question-answering.

## Example Usage

After running the FastAPI server, you can interact with the application using HTTP requests. Here's a simple example:

```bash
curl -X 'POST'   'http://127.0.0.1:8000/get-answer/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "question": "What is AI?"
}'
```

This will return the corresponding answer from the preloaded question-answer database.

## License

MIT License
