from flask import Flask, request, jsonify
from kafka import KafkaProducer
from db.conn import SessionLocal
from email_services import EmailService

import json
import os
import time
app = Flask(__name__)

print(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"))

time.sleep(10) 

producer = KafkaProducer(
    bootstrap_servers=(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@app.route('/api/email', methods=['POST'])
def receive_email():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

   
    producer.send('all_emails', data).get(timeout=30)
    

    return jsonify({"status": "Email sent to Kafka"}), 200


@app.route('/api/email/suspicious', methods=['GET'])
def get_suspicious_email_content():
    email_address = request.args.get('email')
    if not email_address:
        return jsonify({"error": "Email address is required"}), 400

    session = SessionLocal()

    try:
        suspicious_content = EmailService.get_suspicious_content_by_email(session, email_address)
        return jsonify({"suspicious_content": suspicious_content}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    finally:
        session.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
