from kafka import KafkaProducer
import json
import time

KAFKA_TOPIC = "deputes_presence"
KAFKA_BROKER = "localhost:9092"

# Initialiser le Producer Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka():
    with open("deputes_synthese.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for depute in data["deputes"]:
        producer.send(KAFKA_TOPIC, depute["depute"])
        time.sleep(0.1)

    print("Données envoyées à Kafka.")

if __name__ == "__main__":
    send_to_kafka()
