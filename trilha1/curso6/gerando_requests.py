import requests

# GET
urlget = 'https://httpbin.org/get'

resposta = requests.get(urlget)
print(resposta)
print(resposta.text)
# print(resposta.json())

# POST
urlpost = 'https://httpbin.org/post'
data = {"meus_dados": [1, 2, 3],
        "pessoa": {"nome": "Fulano",
                   "profissao": "Professor"}}
params = {"data_inicio": "2024-01-01",
          "data_fim": "2024-12-31"}

resposta = requests.post(urlpost, json=data, params=params)
try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f"Impossível fazer request! Erro: {e}")
else:
    print("Resultado:")
    print(resposta.status_code)
    print(resposta.json())

