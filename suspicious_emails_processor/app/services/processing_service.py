import os
import re
from datetime import datetime
from db.models import EmailModel
from .kafka_service import send_to_partition



KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "all_emails")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
suspicious_keywords = {'hostage': 'messages.hostage', 'explosive': 'messages.explosive'}

def reorder_sentences(sentences, keyword):
    suspicious_sentences = []
    other_sentences = []

    for sentence in sentences:
        if re.search(r'\b' + re.escape(keyword) + r'\b', sentence, re.IGNORECASE):
            suspicious_sentences.append(sentence)
        else:
            other_sentences.append(sentence)

    return suspicious_sentences + other_sentences

def process_message(email_data, session):
    print(f"Processing email: {email_data.get('email', 'unknown@example.com')}")
    email_address = email_data.get('email', 'unknown@example.com')
    username = email_data.get('username', 'unknown')
    received_at = email_data.get('received_at', datetime.now())
    sentences = email_data.get('sentences', [])

    email_obj = session.query(EmailModel).filter_by(email=email_address).first()
    if not email_obj:
        email_obj = EmailModel(email=email_address, username=username, received_at=received_at)
        session.add(email_obj)
        session.commit()

    for sentence in sentences:
        for keyword in suspicious_keywords.keys():
            if re.search(r'\b' + re.escape(keyword) + r'\b', sentence, re.IGNORECASE):
                reordered_sentences = reorder_sentences(sentences, keyword)
                email_data['sentences'] = reordered_sentences
                
                send_to_partition(email_data, keyword)
                print(f"Sent to partition for keyword '{keyword}'")
                break
                
