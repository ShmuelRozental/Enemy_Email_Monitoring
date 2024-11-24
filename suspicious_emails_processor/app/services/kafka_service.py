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





# conn = psycopg2.connect(
#     host=os.getenv("POSTGRES_HOST", "postgres"),
#     database=os.getenv("POSTGRES_DB", "email_monitor"),
#     user=os.getenv("POSTGRES_USER", "postgres"),
#     password=os.getenv("POSTGRES_PASSWORD", "1234")
# )
# cur = conn.cursor()

# def save_suspicious_content(email_id, sentence, keyword):
#     table_name = f"suspicious_{keyword}_content"
#     insert_query = f"INSERT INTO {table_name} (email_id, suspicious_sentence, detected_at) VALUES (%s, %s, %s)"
#     cur.execute(insert_query, (email_id, sentence, datetime.now()))
#     conn.commit()


# def save_suspicious_content(session, email_obj, sentence, keyword):
#     try:
#         if keyword == "hostage":
#             content = HostagesModel(email_details=email_obj, suspicious_sentence=sentence)
#         elif keyword == "explosive":
#             content = ExplosiveModel(email_details=email_obj, suspicious_sentence=sentence)
#         else:
#             raise ValueError(f"Unknown keyword: {keyword}")
        
#         session.add(content)
#         session.commit()
#         print(f"Saved suspicious content to table for {keyword}: {sentence}")
#     except Exception as e:
#         session.rollback()
#         print(f"Error saving to database: {e}")



import os
import json
import re
from kafka import  KafkaConsumer, KafkaProducer

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "all_emails")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
suspicious_keywords = {'hostage': 'messages.hostage', 'explosive': 'messages.explosive'}


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_partition(email_data, keyword):
    try:
        if isinstance(email_data, dict):
            email_data = {k: (v.decode('utf-8') if isinstance(v, bytes) else v) for k, v in email_data.items()}
        producer.send(
            'suspicious_emails',
            key=keyword.encode('utf-8'),
            value=email_data
        ).get(timeout=10)  
        print(f"Suspicious content sent to {suspicious_keywords[keyword]}: {email_data.get('email')}")
    except Exception as e:
        print(f"Error sending to Kafka: {e}")
