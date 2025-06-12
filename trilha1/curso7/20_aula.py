# pip install --upgrade wheel
import os
from io import BytesIO

import speech_recognition as sr
from playsound import playsound

import openai
from dotenv import load_dotenv

_ = load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = openai.Client()

ARQUIVO_AUDIO = 'fala_assistant.mp3'

recognizer = sr.Recognizer()


def grava_audio():
    with sr.Microphone() as source:
        print('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio


def transcricao_audio(audio):
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = 'audio.wav'
    print('Transcrevendo...')
    transcricao = client.audio.transcriptions.create(
        model='whisper-1',
        file=wav_data,
    )
    return transcricao.text


def completa_texto(mensagens):
    print('Gerando resposta...')
    resposta = client.chat.completions.create(
        messages=mensagens,
        # model='gpt-3.5-turbo-0125',
        model='gpt-4.1-nano',
        max_tokens=1000,
        temperature=0
    )
    return resposta


def cria_audio(texto):
    if os.path.exists(ARQUIVO_AUDIO):
        os.remove(ARQUIVO_AUDIO)
        print("Arquivo excluído com sucesso!")
    else:
        print("O arquivo não foi encontrado.")

    print('Gerando audio...')
    resposta = client.audio.speech.create(
        model='tts-1',
        voice='onyx',
        input=texto
    )
    print('Salvando arquivo de audio...')
    resposta.write_to_file(ARQUIVO_AUDIO)


def roda_audio():
    print('Reproduzindo audio...')
    playsound(ARQUIVO_AUDIO)


if __name__ == '__main__':

    mensagens = []

    while True:
        audio = grava_audio()

        transcricao = transcricao_audio(audio)
        mensagens.append({'role': 'user', 'content': transcricao})
        print(f'User: {mensagens[-1]["content"]}')

        # Critério de parada
        if 'encerrar' in mensagens[-1]["content"].lower():
            print('Encerrando...')
            break

        resposta = completa_texto(mensagens)
        mensagens.append({'role': 'assistant', 'content': resposta.choices[0].message.content})
        print(f'Assistant: {mensagens[-1]["content"]}')

        cria_audio(mensagens[-1]["content"])
        roda_audio()
