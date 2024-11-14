# from kafka import KafkaConsumer
# import os
# import json


# suspicious_keywords = {'hostage', 'explosive'}



# consumer = KafkaConsumer(
#     'suspicious_emails',
#     bootstrap_servers=(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")),
#     value_deserializer=lambda v: json.loads(v.decode('utf-8'))
# )

# for message in consumer:
#     email_data = message.value
#     if any(word in email_data.get('sentences', []) for word in suspicious_keywords):
#         print(f"Suspicious email detected: {email_data}")
#     else:
#         print("Email is clean.")




import os
import json
import re
from kafka import KafkaConsumer, KafkaProducer
import psycopg2
from datetime import datetime


suspicious_keywords = {'hostage': 'messages.hostage', 'explosive': 'messages.explosive'}


consumer = KafkaConsumer(
    'suspicious_emails',
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    database=os.getenv("POSTGRES_DB", "email_monitor"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "password")
)
cur = conn.cursor()

def save_suspicious_content(email_id, sentence, keyword):
    table_name = f"suspicious_{keyword}_content"
    insert_query = f"INSERT INTO {table_name} (email_id, suspicious_sentence, detected_at) VALUES (%s, %s, %s)"
    cur.execute(insert_query, (email_id, sentence, datetime.now()))
    conn.commit()

def process_message(email_data):
    email_id = email_data.get('email_id', 'unknown')
    sentences = email_data.get('sentences', [])
    for sentence in sentences:
        for keyword, topic in suspicious_keywords.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', sentence, re.IGNORECASE):
                
                save_suspicious_content(email_id, sentence, keyword)
                
                producer.send(topic, email_data)
                print(f"Suspicious content sent to {topic} and saved to PostgreSQL: {sentence}")

for message in consumer:
    email_data = message.value
    process_message(email_data)


cur.close()
conn.close()
