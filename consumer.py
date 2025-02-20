from kafka import KafkaConsumer
import json

#  Configuration
KAFKA_TOPIC = "deputes_presence"
KAFKA_BROKER = "localhost:9092"

#  Initialisation du Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f" En attente de messages sur le topic {KAFKA_TOPIC}...")

for message in consumer:
    print(f"Depute reçu : {message.value}")
