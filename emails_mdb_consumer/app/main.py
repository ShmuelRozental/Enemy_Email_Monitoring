import time
from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import os
from db.conn import create_mongo_client

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "all_emails")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


try:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
except Exception as e:
    print(f"Failed to connect to Kafka: {e}")
    consumer = None

def load_messages():
    if consumer is None:
        return 'consumer is none'
    collection = create_mongo_client()
    if collection is None:
        return 'collection is none'

    for message in consumer:
        try:
            collection.insert_one(message.value)
            print(f"Inserted message into MongoDB: {message.value}")
        except Exception as e:
            print(f"Failed to insert message into MongoDB: {e}")


if __name__ == "__main__":
    time.sleep(30)
    load_messages()
