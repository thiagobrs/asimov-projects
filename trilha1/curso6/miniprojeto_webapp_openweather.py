import os
import dotenv
import requests
import streamlit as st
from pprint import pprint


def fazer_request(url, params=None):
    resposta = requests.get(url, params=params)

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"Erro no request: {e}.")
        resultado = None
    else:
        resultado = resposta.json()

    return resultado


def pegar_tempo_para_local(local):
    dotenv.load_dotenv() # Carrega as variáveis de ambiente carregadas para o projeto no arquivo .env
    token = os.environ['CHAVE_API_OPENWEATHER']  # API key criada no site da OpenWeather

    # Endpoint para testar uma autenticação bearer (token)
    url = f'https://api.openweathermap.org/data/2.5/weather'

    # Criando um header para autenticação bearer
    params = {
        'appid': token,
        'q': local,
        'units': 'metric',
        'lang': 'pt_br'
    }

    dados_tempo = fazer_request(url, params=params)
    return dados_tempo


def main():
    st.title('Web App Tempo')
    st.write('Powered by OpenWeather (https://openweathermap.org/current)')
    local = st.text_input('Pesquise por uma cidade:')
    if not local:
        st.stop()

    dados_tempo = pegar_tempo_para_local(local)
    if not dados_tempo:
        st.warning(f'Dados não encontrados para a cidade {local}')
        st.stop()

    clima_atual = dados_tempo['weather'][0]['description']
    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    humidade = dados_tempo['main']['humidity']
    cobertura_nuvens = dados_tempo['clouds']['all']

    st.metric(label='Tempo atual', value=clima_atual)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Temperatura', value=f'{temperatura} ºC')
        st.metric(label='Sensação térmica', value=f'{sensacao_termica} ºC')

    with col2:
        st.metric(label='Humidade', value=f'{humidade} %')
        st.metric(label='Cobertura de nuvens', value=f'{cobertura_nuvens} %')


if __name__ == '__main__':
    main()
