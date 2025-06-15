import os
import dotenv
import requests
from fastmcp import FastMCP

servidor_mcp = FastMCP("mcp-busca-tempo")
testing_functions = False


@servidor_mcp.tool()
async def buscar_tempo_atual(local: str) -> dict:
    """
    Busca o tempo atual para o local especificado.
    """
    dotenv.load_dotenv()
    app_id = os.getenv("OPENWEATHER_API_KEY")
    if app_id is None:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": local,
        "appid": app_id,
        "units": "metric",  # Para obter a temperatura em Celsius
        "lang": "pt"  # Para obter a descrição do tempo em português
    }
    response = requests.get(url, params=params)

    return response.json()


@servidor_mcp.tool()
async def buscar_previsao_tempo(local: str) -> dict:
    """
    Busca a previsão do tempo para o local especificado.
    """
    dotenv.load_dotenv()
    app_id = os.getenv("OPENWEATHER_API_KEY")
    if app_id is None:
        raise ValueError("OPENWEATHER_API_KEY environment variable not set")

    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": local,
        "appid": app_id,
        "units": "metric",  # Para obter a temperatura em Celsius
        "lang": "pt"  # Para obter a descrição do tempo em português
    }
    response = requests.get(url, params=params)

    return response.json()


if __name__ == '__main__':
    if testing_functions:
        local = "Recife, BR"
        tempo_atual = buscar_tempo_atual(local)

        print(f"Tempo atual em {local}:")
        print(tempo_atual)

        previsao_tempo = buscar_previsao_tempo(local)
        print(f"\nPrevisão do tempo para {local}:")
        print(previsao_tempo)
    else:
        servidor_mcp.run(transport="sse")


"""
JSON code required to config VS Code to work with this MCP

    "previsao-tempo": {
        "url": "http://127.0.0.1:8000/sse",
        "description": "Um servidor MCP que faz buscas no OpenWeather e retorna valores de sua API."
    }
"""
