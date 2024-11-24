#!/bin/bash

BROKER="kafka:9092"


echo "ממתין לעליית Kafka..."
sleep 10

kafka-topics.sh --create --topic all_emails --bootstrap-server $BROKER --partitions 1 --replication-factor 1
echo "נושא all_emails נוצר."


kafka-topics.sh --create --topic suspicious_emails --bootstrap-server $BROKER --partitions 2 --replication-factor 1
echo "נושא suspicious_emails נוצר."

echo "כל הנושאים נוצרו בהצלחה!"
