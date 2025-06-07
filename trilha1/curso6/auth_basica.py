import base64
import requests
from pprint import pprint

usuario = 'meu-usuario'
senha = 'minha-senha'

# Criar o string de autorização
auth_string = f'{usuario}:{senha}'
print(auth_string)

# Transformar em bytes
auth_string = auth_string.encode()
print(auth_string)

# Codificar para base64
auth_string = base64.b64encode(auth_string)
print(auth_string)

# Desfazer a transformação para bytes
auth_string = auth_string.decode()
print(auth_string)

# Endpoint para testar uma autenticação básica (usuário + senha)
url = 'https://httpbin.org/basic-auth/meu-usuario/minha-senha'

# Criando um header para autenticação básica
headers = {
    'Authorization': f'Basic {auth_string}'
}

resposta = requests.get(url, headers=headers)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f"Erro no request: {e}")
    resultado = None
else:
    resultado = resposta.json()

pprint(resultado)
print(resposta.url)