# import json
# import re
# from db.database import init_db, SessionLocal
# from db.models import EmailModel, HostagesModel, ExplosiveModel
# from consumer import producer, consumer
# from datetime import datetime
# import os
# import time

# init_db()

# def save_suspicious_content(session, email_id, sentence, keyword):
#     if keyword == "hostage":
#         suspicious_content = HostagesModel(email_id=email_id, suspicious_sentence=sentence)
#     elif keyword == "explosive":
#         suspicious_content = ExplosiveModel(email_id=email_id, suspicious_sentence=sentence)
#     session.add(suspicious_content)
#     session.commit()

# def process_message(email_data):
#     session = SessionLocal()
#     email_id = email_data.get('email_id', 'unknown')
#     email = EmailModel(email_id=email_id, email=email_data['email'], username=email_data['username'])
#     session.add(email)
#     session.commit()
    
#     sentences = email_data.get('sentences', [])
#     for sentence in sentences:
#         for keyword, topic in os.geten('SUSPICIOUS_KEYWORDS').items():
#             if re.search(r'\b' + re.escape(keyword) + r'\b', sentence, re.IGNORECASE):
#                 save_suspicious_content(session, email_id, sentence, keyword)
#                 producer.send(topic, email_data)
#                 print(f"Suspicious content sent to {topic} and saved to PostgreSQL: {sentence}")
#     session.close()



# time.sleep(60)
# for message in consumer:
#     email_data = message.value
#     print(email_data)

import time
from services.kafka_service import consumer
from services.processing_service import process_message
from db.conn import init_db, SessionLocal




def main():
    print("Initializing the database...")
    init_db()
    session = SessionLocal()
    try:
        for message in consumer:
            email_data = message.value
            process_message(email_data, session)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()
        print("Database session closed.")

if __name__ == "__main__":
    main()
