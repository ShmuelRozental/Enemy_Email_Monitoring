from kafka import KafkaConsumer
from pymongo import MongoClient
import os
import json


consumer = KafkaConsumer(
    'all_emails',
    bootstrap_servers=(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")),
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)


mongo_client = MongoClient('kafka', 27017)
db = mongo_client['email_monitor']
collection = db['all_messages']

for message in consumer:
    collection.insert_one(message.value)
    print(f"Inserted message into MongoDB: {message.value}")
