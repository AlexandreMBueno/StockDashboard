import streamlit as st
import pandas as pd
import requests as req
import altair as alt
from datetime import datetime, timedelta

def ler_chave():
    with open('chave.txt', 'r') as file:
        for line in file:
            if line.startswith('chave_ab'):
                return line.split('=')[1].strip()
    return None


# primeira requisicao feita para todos os tickers
URL_BASE = 'https://api.fintz.com.br'
HEADERS = { 'X-API-Key': ler_chave() }
PARAMS = {'classe': 'ACOES', 'ativo': 'true'}


endpoint = URL_BASE + '/bolsa/b3/avista/busca'
res = req.get(endpoint, headers=HEADERS, params=PARAMS)
response_data = res.json()


# Extrair todos os tickers
todos_tickers = [item['ticker'] for item in response_data]


ticker = st.sidebar.selectbox('Selecione um ticker', todos_tickers)
data_default = (datetime.today() - timedelta(days=30))
dataInicio = st.sidebar.date_input('Start Date', value=data_default).strftime('%Y-%m-%d')
dataFim = st.sidebar.date_input('End Date', value=datetime.today()).strftime('%Y-%m-%d')
