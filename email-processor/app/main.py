from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os

app = Flask(__name__)

print(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"))

producer = KafkaProducer(
    bootstrap_servers=(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@app.route('/api/email', methods=['POST'])
def receive_email():
    data = request.json
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

   
    producer.send('all_emails', data).get(timeout=30)
    producer.send('suspicious_emails', data).get(timeout=30)

    return jsonify({"status": "Email sent to Kafka"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
