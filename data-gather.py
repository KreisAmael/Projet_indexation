import requests
import json
import time

# URL de l'API NosDéputés.fr
API_URL = "https://www.nosdeputes.fr/synthese/data/json"

# Fichier de sauvegarde local
OUTPUT_FILE = "deputes_synthese.json"

def download_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
        
        print(f"✅ Données téléchargées et mises à jour dans {OUTPUT_FILE}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    while True:
        download_data()
        time.sleep(86400)
