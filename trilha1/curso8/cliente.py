import os
import dotenv
import asyncio
# from pathlib import Path
import openai
from fastmcp import Client

# caminho_servidor = Path(__file__).parent / "servidor.py"  # Se o servidor estiver no mesmo diretório
caminho_servidor = 'http://127.0.0.1:8000/sse'  # Se o servidor estiver no mesmo diretório
cliente = Client(caminho_servidor)


async def testar_servidor(cliente, busca):
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    async with cliente:
        argumentos = {"busca": busca}
        resposta = await cliente.call_tool("buscar_wikipedia", arguments=argumentos)
        print(resposta)

        mensagem_sistema = f"""
            Você é um bot que faz buscas na wikipedia. O usuário buscou pelo seguinte tema: {busca}.
            Para esta busca, você recebeu a seguinte resposta: {resposta}.
            Com base nesse conteúdo, você deve responder ao usuário com uma mensagem amigável e informativa.
        """

        cliente_openai = openai.OpenAI()
        response = cliente_openai.responses.create(
            model='gpt-4o-mini',
            instructions=mensagem_sistema,
            input='Pode me falar mais sobre isso?'
        )
        print(response.output_text)


async def testar_servidor_tempo(cliente, local):
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    async with cliente:
        argumentos = {"local": local}
        tempo_atual = await cliente.call_tool("buscar_tempo_atual", arguments=argumentos)
        previsao_tempo = await cliente.call_tool("buscar_previsao_tempo", arguments=argumentos)

        mensagem_sistema = f"""
            Você é um bot que faz buscas de previsão do tempo e sintetiza a resposta.
            O usuário buscou pela previsão no seguinte local: {local}.
            Para esta busca, você recebeu a seguinte resposta: {previsao_tempo}.
            Além disso, o tempo atual é: {tempo_atual}.
            Com base nesse conteúdo, você deve responder ao usuário com uma mensagem amigável e informativa.
        """

        cliente_openai = openai.OpenAI()
        response = cliente_openai.responses.create(
            model='gpt-4o-mini',
            instructions=mensagem_sistema,
            input='Qual a previsão do tempo no local indicado?'
        )
        print(response.output_text)


if __name__ == '__main__':
    asyncio.run(testar_servidor_tempo(
        cliente=cliente,
        local="Recife, BR")
    )
