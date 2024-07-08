''' Descricao -->
Endpoint que fornece os dados históricos de cotação dos ativos negociados na B3.
Formato OHLC (Open - High - Low - Close) para o ticker especificado e dentro do intervalo de datas determinado.
'''
import streamlit as st
import pandas as pd
import requests as req
import altair as alt # arrumar data e ver valores corretos no grafico
from datetime import datetime, timedelta
import time

# funcao para ler a chave de chave.txt

def ler_chave():
    with open('chave.txt', 'r') as file:
        for line in file:
            if line.startswith('chave_ab'):
                return line.split('=')[1].strip()
    return None

data_default = (datetime.today() - timedelta(days=30)) # data padrao sera a de hoje menos 30 dias (ultimo mes)

ticker = st.sidebar.text_input('Ticker', value = 'BBAS3').upper()
dataInicio = st.sidebar.date_input('Start Date', value = data_default)
dataFim = st.sidebar.date_input('End Date', value = datetime.today())
with st.spinner('Aguarde um momento...'):
    time.sleep(3)
st.success('Pronto!')

if not ticker:
    st.error('Por favor insira um ticker valido.', icon="🚨")


# Convertendo as datas para string no formato correto
dataInicio = dataInicio.strftime('%Y-%m-%d')
dataFim = dataFim.strftime('%Y-%m-%d')


URL_BASE = 'https://api.fintz.com.br'
HEADERS = { 'X-API-Key': ler_chave() }
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio, 'dataFim': dataFim} # dataFim opcional

# fazer requisicao na url com os parametro passados
endpoint = URL_BASE + '/bolsa/b3/avista/cotacoes/historico'
res = req.get(endpoint, headers=HEADERS, params=PARAMS)


resposta = res.json()
precos_fechamento_ajustado = [item['precoFechamentoAjustado'] for item in resposta]
datas = [item['data'] for item in resposta]

# DATAFRAME

df = pd.DataFrame({
    'Data': datas,
    'PrecoFechamentoAjustado': precos_fechamento_ajustado
})

df['Data'] = pd.to_datetime(df['Data']).dt.date

df.set_index('Data', inplace=True)

df = df.iloc[::-1] # dados em ordem

clciked = st.sidebar.button("ENTER")
st.title(f'Fintz Stock Dashboard - {ticker}')
st.title(f"DF - {ticker}")
st.write(df)

# -------------- Grafico linha

chart = alt.Chart(df.reset_index()).mark_line(point=True).encode(
    x=alt.X('Data:T', title='Data', axis=alt.Axis(format='%Y-%m-%d', labelAngle=-90)), # seta eixo x como data e o T maisculo serve para dizer que sao do tipo datetime
    y=alt.Y('PrecoFechamentoAjustado:Q', title='Preço de Fechamento Ajustado', scale=alt.Scale(zero=False)), # scale para grafico se ajustar ao valor
    tooltip=['Data:T', 'PrecoFechamentoAjustado'] # p passar mouse em cima dos pontos e mostrar valor e data exatos
)#.interactive() se quiser dar zoom

#plotando grafico
st.title(f'Grafico de linha - {ticker}')
st.altair_chart(chart, use_container_width=True) # aumentar grafico


#--------    Indicadores

# URL_BASE = 'https://api.fintz.com.br'
# HEADERS = { 'X-API-Key': 'chave-de-teste-api-fintz' }
PARAMS = { 'ticker': ticker }

endpoint_indicadores = URL_BASE + '/bolsa/b3/avista/indicadores/por-ticker'
res_indicadores = req.get(endpoint_indicadores, headers=HEADERS, params=PARAMS)


dados_indicadores = res_indicadores.json()
df_res_indicadores = pd.DataFrame(dados_indicadores)

st.title(f'Indicadores - {ticker}')
st.table(df_res_indicadores)


# --------- Proventos

# URL_BASE = 'https://api.fintz.com.br'
# HEADERS = { 'X-API-Key': 'chave-de-teste-api-fintz' }
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio}

endpoint_proventos = URL_BASE + '/bolsa/b3/avista/proventos'
res_proventos = req.get(endpoint_proventos, headers=HEADERS, params=PARAMS)
# print(res_proventos.json())
dados_proventos = res_proventos.json()
df_res_proventos = pd.DataFrame(dados_proventos)

st.title(f'Eventos - Proventos - {ticker}')
st.table(df_res_proventos)


# -------- Bonificacoes

# URL_BASE = 'https://api.fintz.com.br'
# HEADERS = { 'X-API-Key': 'chave-de-teste-api-fintz' }
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio }

endpoint_bonificacoes = URL_BASE + '/bolsa/b3/avista/bonificacoes'
res_bonificacoes = req.get(endpoint_bonificacoes, headers=HEADERS, params=PARAMS)
# print(res_bonificacoes.json())

dados_bonificacoes = res_bonificacoes.json()
df_res_bonificacoes = pd.DataFrame(dados_bonificacoes)

st.title(f'Bonificacoes - {ticker}')
st.table(df_res_bonificacoes)

# -------- Desdobramentos

# URL_BASE = 'https://api.fintz.com.br'
# HEADERS = { 'X-API-Key': 'chave-de-teste-api-fintz' }
PARAMS = { 'ticker': ticker, 'dataInicio': dataInicio }

endpoint_desdobramentos = URL_BASE + '/bolsa/b3/avista/desdobramentos'
res_desdobramentos = req.get(endpoint_desdobramentos, headers=HEADERS, params=PARAMS)

dados_desdobramentos = res_desdobramentos.json()
df_res_desdobramentos = pd.DataFrame(dados_desdobramentos)

st.title(f'Desdobramentos - {ticker}')
st.table(df_res_desdobramentos)