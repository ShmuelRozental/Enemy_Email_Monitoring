from kafka import KafkaConsumer
from pymongo import MongoClient
import json


consumer = KafkaConsumer(
    'all_emails',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)


mongo_client = MongoClient('localhost', 27017)
db = mongo_client['email_monitor']
collection = db['all_messages']

for message in consumer:
    collection.insert_one(message.value)
    print(f"Inserted message into MongoDB: {message.value}")
