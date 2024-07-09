''' Descricao -->
Endpoint que fornece os dados históricos de cotação dos ativos negociados na B3.
Formato OHLC (Open - High - Low - Close) para o ticker especificado e dentro do intervalo de datas determinado.
'''
import streamlit as st
import pandas as pd
import requests as req
import altair as alt
from datetime import datetime, timedelta
import time


# ----- Funcao p ler api-key
def ler_chave():
    with open('chave.txt', 'r') as file:
        for line in file:
            if line.startswith('chave_ab'):
                return line.split('=')[1].strip()
    return None


# ----- Default URL BASE e HEADERS 
URL_BASE = 'https://api.fintz.com.br'
HEADERS = { 'X-API-Key': ler_chave() }


# ----- Request todos os tickers
PARAMS = {'classe': 'ACOES', 'ativo': 'true'}

endpoint = URL_BASE + '/bolsa/b3/avista/busca'
res = req.get(endpoint, headers=HEADERS, params=PARAMS)
response_data = res.json()

todos_tickers = [item['ticker'] for item in response_data]
ticker = st.sidebar.selectbox('Selecione um ticker', todos_tickers)
data_default = (datetime.today() - timedelta(days=30))
dataInicio = st.sidebar.date_input('Start Date', value=data_default).strftime('%Y-%m-%d')
dataFim = st.sidebar.date_input('End Date', value=datetime.today()).strftime('%Y-%m-%d')


# UI Features
with st.spinner('Aguarde um momento...'):
    time.sleep(3)
st.success('Pronto!')

if not ticker:
    st.error('Por favor insira um ticker valido.', icon="🚨")


# ----- Request precoFechamentoAjustado
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio, 'dataFim': dataFim} # dataFim opcional

endpoint = URL_BASE + '/bolsa/b3/avista/cotacoes/historico'
res = req.get(endpoint, headers=HEADERS, params=PARAMS)

resposta = res.json()
precos_fechamento_ajustado = [item['precoFechamentoAjustado'] for item in resposta]
datas = [item['data'] for item in resposta]


# ----- DATAFRAME
df = pd.DataFrame({
    'Data': datas,
    'PrecoFechamentoAjustado': precos_fechamento_ajustado
})

df['Data'] = pd.to_datetime(df['Data']).dt.date
df.set_index('Data', inplace=True)
df = df.iloc[::-1]

clciked = st.sidebar.button("ENTER")
st.title(f'Stock Dashboard - {ticker}')
st.title(f"DF - {ticker}")
st.write(df)


# ------ Grafico linha
chart = alt.Chart(df.reset_index()).mark_line(point=True).encode(
    x=alt.X('Data:T', title='Data', axis=alt.Axis(format='%Y-%m-%d', labelAngle=-90)),
    y=alt.Y('PrecoFechamentoAjustado:Q', title='Preço de Fechamento Ajustado', scale=alt.Scale(zero=False)),
    tooltip=['Data:T', 'PrecoFechamentoAjustado']
 ).interactive()

st.title(f'Grafico de linha - {ticker}')
st.altair_chart(chart, use_container_width=True)


# ----- Indicadores
PARAMS = { 'ticker': ticker }

endpoint_indicadores = URL_BASE + '/bolsa/b3/avista/indicadores/por-ticker'
res_indicadores = req.get(endpoint_indicadores, headers=HEADERS, params=PARAMS)

dados_indicadores = res_indicadores.json()
df_res_indicadores = pd.DataFrame(dados_indicadores)

st.title(f'Indicadores - {ticker}')
st.table(df_res_indicadores)


# ----- Proventos
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio}

endpoint_proventos = URL_BASE + '/bolsa/b3/avista/proventos'
res_proventos = req.get(endpoint_proventos, headers=HEADERS, params=PARAMS)

dados_proventos = res_proventos.json()
df_res_proventos = pd.DataFrame(dados_proventos)

st.title(f'Eventos - Proventos - {ticker}')
st.table(df_res_proventos)


# ----- Request Bonificacoes
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio }

endpoint_bonificacoes = URL_BASE + '/bolsa/b3/avista/bonificacoes'
res_bonificacoes = req.get(endpoint_bonificacoes, headers=HEADERS, params=PARAMS)

dados_bonificacoes = res_bonificacoes.json()
df_res_bonificacoes = pd.DataFrame(dados_bonificacoes)

st.title(f'Bonificacoes - {ticker}')
st.table(df_res_bonificacoes)


# ----- Request Desdobramentos
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio }

endpoint_desdobramentos = URL_BASE + '/bolsa/b3/avista/desdobramentos'
res_desdobramentos = req.get(endpoint_desdobramentos, headers=HEADERS, params=PARAMS)

dados_desdobramentos = res_desdobramentos.json()
df_res_desdobramentos = pd.DataFrame(dados_desdobramentos)

st.title(f'Desdobramentos - {ticker}')
st.table(df_res_desdobramentos)