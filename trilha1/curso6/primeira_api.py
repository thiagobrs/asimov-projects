from pprint import pprint
import requests

nome = "Eduarda"
url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
params = {
    'sexo': 'F',
    'localidade': 33
}

resposta = requests.get(url, params=params)

print(resposta.request.url)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f"Erro no request: {e}.")
    resultado = None
else:
    resultado = resposta.json()
    pprint(resultado[0]['res'])
