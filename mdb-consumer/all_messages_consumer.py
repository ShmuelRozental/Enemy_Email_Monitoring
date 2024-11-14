from kafka import KafkaConsumer
from pymongo import MongoClient
import os
import json


KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "all_emails")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "email_monitor")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "all_messages")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)


mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

for message in consumer:
    try:
        collection.insert_one(message.value)
        print(f"Inserted message into MongoDB: {message.value}")
    except Exception as e:
        print(f"Failed to insert message into MongoDB: {e}")
