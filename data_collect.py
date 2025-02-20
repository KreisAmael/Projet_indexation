import requests
import json
import time
from kafka import KafkaProducer

# Configuration
API_URL = "https://www.nosdeputes.fr/synthese/data/json"
KAFKA_TOPIC = "deputes_presence"
KAFKA_BROKER = "localhost:9092"
INTERVAL = 86400  # 24 heures en secondes

# Initialisation du Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_data():
    """Telecharge les donnees depuis l'API NosDeputes.fr."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        print(" Donnees recuperees depuis l'API.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recuperation des donnees : {e}")
        return None

def send_to_kafka(data):
    """Envoie les donnees à Kafka."""
    if not data or "deputes" not in data:
        print("Aucune donnee valide à envoyer à Kafka.")
        return
    
    for depute in data["deputes"]:
        producer.send(KAFKA_TOPIC, depute["depute"])
        time.sleep(0.1)  # Petit delai pour eviter la surcharge du broker
    
    print(f"Donnees envoyees à Kafka ({len(data['deputes'])} deputes).")

if __name__ == "__main__":
    while True:
        print("Debut d'une nouvelle extraction...")
        data = fetch_data()
        send_to_kafka(data)
        print(f" Pause de {INTERVAL // 3600} heures avant la prochaine extraction.\n")
        time.sleep(INTERVAL)  # Attendre 24 heures avant la prochaine execution
