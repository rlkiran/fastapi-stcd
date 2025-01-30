from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from db import load_data_from_mongo

# Initialize variables for models and clustering
model = None
kmeans = None
embeddings = None
questions = []
answers = []

def map_clusters_to_answers(kmeans, embeddings, questions, answers):
    cluster_to_answer = {}
    clusters = kmeans.labels_

    for cluster_id in range(len(answers)):
        cluster_questions = [questions[i] for i in range(len(questions)) if clusters[i] == cluster_id]
        cluster_embeddings = [embeddings[i] for i in range(len(questions)) if clusters[i] == cluster_id]
        centroid = kmeans.cluster_centers_[cluster_id]
        closest_idx = cdist([centroid], cluster_embeddings).argmin()
        closest_question = cluster_questions[closest_idx]
        cluster_to_answer[cluster_id] = answers[0 if closest_question in questions[:2] else 1]

    return cluster_to_answer

def get_answer(question: str):
    embedding = model.encode([question])
    cluster = kmeans.predict(embedding)[0]
    cluster_to_answer = map_clusters_to_answers(kmeans, embeddings, questions, answers)
    return cluster_to_answer.get(cluster, "Answer not found.")

# Proper async context manager for preloading models
from contextlib import asynccontextmanager

@asynccontextmanager
async def preload_models(app):
    global model, kmeans, embeddings, questions, answers
    
    # Load questions and answers from MongoDB
    questions, answers = load_data_from_mongo()
    
    # Load the model and perform clustering
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(questions)  # Generate embeddings for questions

    # Apply KMeans clustering
    num_clusters = len(answers)  # Assume each cluster corresponds to one answer
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)

    # Set the models globally for access
    app.state.model = model
    app.state.kmeans = kmeans
    app.state.embeddings = embeddings

    # Yield control back to FastAPI to indicate startup is complete
    yield
