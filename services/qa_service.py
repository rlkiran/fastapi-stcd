from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from db import load_data_from_mongo
from contextlib import asynccontextmanager

model = None
kmeans = None
cluster_to_answer = {}

def map_clusters_to_answers(kmeans, embeddings, questions, answers):
    """Maps each cluster to the closest question-answer pair."""
    cluster_to_answer = {}
    clusters = kmeans.labels_
    
    for cluster_id in set(clusters):
        cluster_indices = [i for i in range(len(questions)) if clusters[i] == cluster_id]
        if not cluster_indices:
            continue  # Skip empty clusters

        # Get embeddings of questions in this cluster
        cluster_embeddings = [embeddings[i] for i in cluster_indices]
        centroid = kmeans.cluster_centers_[cluster_id]

        # Find the closest question to the centroid
        closest_idx = cluster_indices[cdist([centroid], cluster_embeddings).argmin()]
        cluster_to_answer[cluster_id] = answers[closest_idx]  # Assign correct answer

    return cluster_to_answer

def get_answer(question: str):
    """Returns the best-matching answer based on clustering."""
    if model is None or kmeans is None or not cluster_to_answer:
        return "Model is not loaded yet. Try again later."

    embedding = model.encode([question])
    cluster = kmeans.predict(embedding)[0]
    return cluster_to_answer.get(cluster, "Answer not found.")

@asynccontextmanager
async def preload_models(app):
    """Loads the model, clusters questions, and prepares cluster-to-answer mapping."""
    global model, kmeans, cluster_to_answer
    
    # Load questions and answers from MongoDB
    questions, answers = load_data_from_mongo()
    
    # Ensure valid data
    if not questions or not answers:
        print("Warning: No data found in MongoDB!")
        yield
        return

    # Load model and generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(questions)

    # Determine optimal cluster count
    num_clusters = min(len(set(answers)), len(questions))  # Prevent excessive clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(embeddings)

    # Precompute cluster-to-answer mapping
    cluster_to_answer = map_clusters_to_answers(kmeans, embeddings, questions, answers)

    # Store models in FastAPI state
    app.state.model = model
    app.state.kmeans = kmeans

    yield  # Allow FastAPI startup to continue
