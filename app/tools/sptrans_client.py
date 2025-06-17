import requests
import os

BASE_URL = "http://api.olhovivo.sptrans.com.br/v2.1"
API_KEY = os.getenv("SPTRANS_API_KEY")
session = requests.Session()

def authenticate():
    auth_url = f"{BASE_URL}/Login/Autenticar?token={API_KEY}"
    try:
        response = session.post(auth_url)
        if response.status_code == 200 and response.text.lower() == 'true':
            return True
        print(f"SPTrans Auth Failed: {response.text}")
        return False
    except Exception as e:
        print(f"SPTrans Connection Error: {e}")
        return False

def search_line(term: str):
    search_url = f"{BASE_URL}/Linha/Buscar?termosBusca={term}"
    response = session.get(search_url)
    return response.json() if response.status_code == 200 else None

def get_bus_positions(line_code: int):
    positions_url = f"{BASE_URL}/Posicao?codigoLinha={line_code}"
    response = session.get(positions_url)
    return response.json() if response.status_code == 200 else None

# Tenta autenticar na inicialização
authenticate()