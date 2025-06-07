import os
import dotenv
import requests
from pprint import pprint

dotenv.load_dotenv() # Carrega as variáveis de ambiente carregadas para o projeto no arquivo .env
token = os.environ['CHAVE_API_OPENWEATHER']  # API key criada no site da OpenWeather

print(token)

# Endpoint para testar uma autenticação do tipo bearer com api key
url = f'https://api.openweathermap.org/data/2.5/weather'

# Criando um header para autenticação bearer
params = {
    'appid': token,
    'q': 'Recife,BR',
    'units': 'metric'
}

resposta = requests.get(url, params=params)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f"Erro no request: {e}")
    resultado = None
else:
    resultado = resposta.json()

pprint(resultado)
print(resposta.url)
