from kafka import KafkaConsumer
import os
import json


suspicious_keywords = {'suspicious', 'fraud', 'scam'}


consumer = KafkaConsumer(
    'suspicious_emails',
    bootstrap_servers=(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")),
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    email_data = message.value
    if any(word in email_data.get('sentences', []) for word in suspicious_keywords):
        print(f"Suspicious email detected: {email_data}")
    else:
        print("Email is clean.")
