''' Descricao -->
Endpoint que fornece os dados históricos de cotação dos ativos negociados na B3.
Formato OHLC (Open - High - Low - Close) para o ticker especificado e dentro do intervalo de datas determinado.
'''
import streamlit as st
import pandas as pd
import requests as req
import altair as alt # arrumar data e ver valores corretos no grafico
from datetime import datetime, timedelta

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

st.title(f'Fintz Stock Dashboard - {ticker}')
st.title(f"DF - {ticker}")
st.write(df)

# GRAFICO

chart = alt.Chart(df.reset_index()).mark_line(point=True).encode(
    x=alt.X('Data:T', title='Data', axis=alt.Axis(format='%Y-%m-%d', labelAngle=-90)), # seta eixo x como data e o T maisculo serve para dizer que sao do tipo datetime
    y=alt.Y('PrecoFechamentoAjustado:Q', title='Preço de Fechamento Ajustado', scale=alt.Scale(zero=False)), # scale para grafico se ajustar ao valor
    tooltip=['Data:T', 'PrecoFechamentoAjustado'] # p passar mouse em cima dos pontos e mostrar valor e data exatos
)#.interactive() se quiser dar zoom

#plotando grafico
st.title(f'Line Chart - {ticker}')
st.altair_chart(chart, use_container_width=True) # aumentar grafico

