# db.py

from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Change this if needed
db = client['qa_database']  # Use the 'qa_database' database
collection = db['qa_collection']  # Use the 'qa_collection' collection

# Function to load questions and answers from MongoDB
def load_data_from_mongo():
    questions = []
    answers = []
    data = collection.find()  # Retrieve all data from the collection
    for item in data:
        questions.append(item['question'])
        answers.append(item['answer'])
    return questions, answers
