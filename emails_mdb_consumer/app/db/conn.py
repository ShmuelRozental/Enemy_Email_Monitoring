from pymongo import MongoClient
import os


def create_mongo_client():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:1234@mongo:27017/email_monitor?authSource=admin")
    MONGO_DB = os.getenv("MONGO_DB", "email_monitor")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "all_messages")
    
    try:
        mongo_client = MongoClient(MONGO_URI)
        db = mongo_client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        print("Connected to MongoDB!")
        return collection
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None