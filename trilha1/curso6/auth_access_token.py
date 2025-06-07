import os
import dotenv
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint

dotenv.load_dotenv() # Carrega as variáveis de ambiente carregadas para o projeto no arquivo .env
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

# Autenticação basic para pegar o token
auth = HTTPBasicAuth(username=client_id, password=client_secret)
url = 'https://accounts.spotify.com/api/token'

# Criando um body que indica para o spotify a operação que desejamos realizar
body = {
    'grant_type': 'client_credentials'
}

resposta = requests.post(url, data=body, auth=auth)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f"Erro no request: {e}")
    resultado = None
else:
    resultado = resposta.json()

# Autenticação bearer para fazer chamadas à api
token = resultado['access_token']

id_artista = '2QsynagSdAqZj3U9HgDzjD'
url = f'https://api.spotify.com/v1/artists/{id_artista}'
headers = {
    'Authorization': f'Bearer {token}'
}

resposta = requests.get(url, headers=headers)
pprint(resposta.json())
