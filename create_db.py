# create_db.py

from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Change this if needed
db = client['qa_database']  # Use the 'qa_database' database
collection = db['qa_collection']  # Use the 'qa_collection' collection

# Function to insert multiple question-answer pairs
def insert_qa_pairs():
    qa_pairs = [
        {"question": "What is AI?", "answer": "AI is Artificial Intelligence."},
        {"question": "Explain AI", "answer": "Artificial Intelligence (AI) is the simulation of human intelligence in machines."},
        {"question": "What is machine learning?", "answer": "Machine learning (ML) is a subset of AI focused on learning from data."},
        {"question": "Define ML", "answer": "Machine learning refers to algorithms that allow systems to learn from data and improve over time."},
        {"question": "How does AI work?", "answer": "AI works by processing large amounts of data, recognizing patterns, and making decisions with minimal human intervention."},
        {"question": "What are the uses of machine learning?", "answer": "Machine learning is used in various fields like finance, healthcare, autonomous vehicles, and recommendation systems."},
        {"question": "What is deep learning?", "answer": "Deep learning is a subset of machine learning that uses neural networks with many layers to analyze various data types."},
        {"question": "What are neural networks?", "answer": "Neural networks are algorithms inspired by the human brain, used for pattern recognition, classification, and prediction."},
        {"question": "What is supervised learning?", "answer": "Supervised learning is a type of machine learning where the model is trained on labeled data."},
        {"question": "What is unsupervised learning?", "answer": "Unsupervised learning is a type of machine learning where the model is trained on unlabeled data, often used for clustering or association tasks."},
        {"question": "What is reinforcement learning?", "answer": "Reinforcement learning is a type of machine learning where an agent learns by interacting with its environment to maximize a reward."}
    ]
    
    # Insert the QA pairs into the MongoDB collection
    collection.insert_many(qa_pairs)
    print("Data inserted successfully!")

# Call the function to insert data
if __name__ == "__main__":
    insert_qa_pairs()
