import re
from db.database import init_db, SessionLocal
from db.models import EmailModel, HostagesModel, ExplosiveModel
from kafka.consumer import consumer
from kafka.producer import producer
import config
from datetime import datetime


init_db()

def save_suspicious_content(session, email_id, sentence, keyword):
    if keyword == "hostage":
        suspicious_content = HostagesModel(email_id=email_id, suspicious_sentence=sentence)
    elif keyword == "explosive":
        suspicious_content = ExplosiveModel(email_id=email_id, suspicious_sentence=sentence)
    session.add(suspicious_content)
    session.commit()

def process_message(email_data):
    session = SessionLocal()
    email_id = email_data.get('email_id', 'unknown')
    email = EmailModel(email_id=email_id, email=email_data['email'], username=email_data['username'])
    session.add(email)
    session.commit()
    
    sentences = email_data.get('sentences', [])
    for sentence in sentences:
        for keyword, topic in config.SUSPICIOUS_KEYWORDS.items():
            if re.search(r'\b' + re.escape(keyword) + r'\b', sentence, re.IGNORECASE):
                save_suspicious_content(session, email_id, sentence, keyword)
                producer.send(topic, email_data)
                print(f"Suspicious content sent to {topic} and saved to PostgreSQL: {sentence}")
    session.close()

for message in consumer:
    email_data = message.value
    process_message(email_data)
