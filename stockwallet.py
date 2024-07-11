import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
import requests as req
from datetime import datetime, timedelta

# ----- Função para ler a chave da API
def ler_chave():
    with open('chave.txt', 'r') as file:
        for line in file:
            if line.startswith('chave_ab'):
                return line.split('=')[1].strip()
    return None

# ----- URL base e headers
URL_BASE = 'https://api.fintz.com.br'
HEADERS = {'X-API-Key': ler_chave()}

# ----- request preco fechamento ajustado
def obter_precos(ticker, data_inicio, data_fim):
    endpoint = f"{URL_BASE}/bolsa/b3/avista/cotacoes/historico"
    params = {'ticker': ticker, 'dataInicio': data_inicio, 'dataFim': data_fim}
    res = req.get(endpoint, headers=HEADERS, params=params)
    return [(item['data'], item['precoFechamentoAjustado']) for item in res.json()]

# ----- request todos os ticker
def obter_todos_tickers():
    endpoint = f"{URL_BASE}/bolsa/b3/avista/busca"
    params = {'classe': 'ACOES', 'ativo': 'true'}
    res = req.get(endpoint, headers=HEADERS, params=params)
    return [item['ticker'] for item in res.json()]

todos_tickers = obter_todos_tickers()

st.sidebar.title('Adicionar Ativo')
ticker = st.sidebar.selectbox('Selecione um ticker', todos_tickers)
quantidade = st.sidebar.number_input('Quantidade', min_value=1, step=1)
valor_pago = st.sidebar.number_input('Valor Pago (por ação)', min_value=0.01, step=0.01)
data_compra = st.sidebar.date_input('Data de Compra', value=datetime.today()).strftime('%Y-%m-%d')
adicionar = st.sidebar.button('Adicionar Ativo')

data_fim = st.sidebar.date_input('Data Fim', value=datetime.today()).strftime('%Y-%m-%d')

# ----- lista de ativos q o usuario passa
if 'ativos' not in st.session_state: # essa session_state e padrao do streamlit p dados q o usuario digitaa
    st.session_state['ativos'] = []

if adicionar:
    st.session_state['ativos'].append({'ticker': ticker, 'quantidade': quantidade, 'valor_pago': valor_pago, 'data_compra': data_compra})

ativos = st.session_state['ativos']

# ativos_consolidados = dict que armazena a qntd total e o valor total pago para cada ticker
ativos_consolidados = {} # isso serve p consolidar todas as compras de um mesmo ativo, transacoes, qntd e valores pagos em uma entrada so
for ativo in ativos:

    ticker = ativo['ticker']
    if ticker not in ativos_consolidados:
        ativos_consolidados[ticker] = {'quantidade': 0, 'valor_total_pago': 0}
    ativos_consolidados[ticker]['quantidade'] += ativo['quantidade']
    ativos_consolidados[ticker]['valor_total_pago'] += ativo['quantidade'] * ativo['valor_pago']

valores_iniciais = []
valores_finais = []
valores_medios_pagos = []
valores_fechamento_atuais = []
quantidades = []
tickers = []

for ticker, dados in ativos_consolidados.items():
    quantidade = dados['quantidade']
    valor_total_pago = dados['valor_total_pago']
    valor_medio_pago = valor_total_pago / quantidade

    historico = obter_precos(ticker, ativos[0]['data_compra'], data_fim)
    valor_fechamento_atual = historico[0][1] if historico else 0
    valor_final = quantidade * valor_fechamento_atual

    valores_iniciais.append(valor_total_pago)
    valores_medios_pagos.append(round(valor_medio_pago, 2))
    valores_finais.append(valor_final)
    valores_fechamento_atuais.append(valor_fechamento_atual)
    quantidades.append(quantidade)
    tickers.append(ticker)

valor_inicial_total = sum(valores_iniciais)
valor_final_total = sum(valores_finais)
rendimento_total = ((valor_final_total - valor_inicial_total) / valor_inicial_total * 100) if valor_inicial_total != 0 else 0

st.sidebar.write(f'Valor inicial: R$ {valor_inicial_total:,.2f}')
st.sidebar.write(f'Valor final: R$ {valor_final_total:,.2f}')
st.sidebar.write(f'Rendimento da carteira: {rendimento_total:.2f}%')

df_resumo = pd.DataFrame({
    'Ticker': tickers,
    'Quantidade': quantidades,
    'Valor Médio Pago R$': valores_medios_pagos,
    'Valor Fechamento Atual R$': valores_fechamento_atuais,
    'Valor Aplicado Total R$': [f"{valor:,.2f}" for valor in valores_iniciais],
    'Valor Final Total R$': [f"{valor:,.2f}" for valor in valores_finais],
    'Rendimento %': [(final - inicial) / inicial * 100 if inicial != 0 else 0 for final, inicial in zip(valores_finais, valores_iniciais)]
})

menu_opcoes = option_menu(
    menu_title=None,
    options=["Resumo", "Gráficos"],
    default_index=0,
    orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "rgb(46, 134, 222)"}}
)

st.title('Carteira de Ações')

if menu_opcoes == 'Gráficos':
    st.subheader('Distribuição das Ações na Carteira')
    fig, ax = plt.subplots()
    percentuais = [(valor / sum(valores_finais)) * 100 for valor in valores_finais]
    ax.pie(percentuais, labels=tickers, startangle=90, wedgeprops=dict(width=0.35))
    ax.axis('equal')
    st.pyplot(fig)

elif menu_opcoes == 'Resumo':
    st.subheader(f'Resumo das Ações\n {data_fim}')
    st.dataframe(df_resumo)
