import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
import requests as req
from datetime import datetime, timedelta

# Funcao para ler a chave da API
def ler_chave():
    with open('chave.txt', 'r') as file:
        for line in file:
            if line.startswith('chave_ab'):
                return line.split('=')[1].strip()
    return None

# URL base e headers
URL_BASE = 'https://api.fintz.com.br'
HEADERS = {'X-API-Key': ler_chave()}

# ----- Request Preco Fechamento Ajustado
def obter_precos(ticker, data_inicio, data_fim):
    params = {'ticker': ticker, 'dataInicio': data_inicio, 'dataFim': data_fim}
    endpoint = URL_BASE + '/bolsa/b3/avista/cotacoes/historico'
    res = req.get(endpoint, headers=HEADERS, params=params)
    resposta = res.json()
    return [(item['data'], item['precoFechamentoAjustado']) for item in resposta]


carteiras = {
    'Carteira 1': {'Acoes': ['RENT3', 'BBAS3', 'CXSE3'], 'Quantidade': [150, 100, 250]},
    'Carteira 2': {'Acoes': ['PETR4', 'VALE3', 'ITUB4'], 'Quantidade': [200, 150, 300]},
    'Carteira 3': {'Acoes': ['ABEV3', 'BBDC4', 'ITSA4'], 'Quantidade': [250, 200, 150]}
}

# sidebar com seleionar carteira e datas
carteira_selecionada = st.sidebar.selectbox('Selecione a carteira', list(carteiras.keys()))
carteira = carteiras[carteira_selecionada]
data_inicio = st.sidebar.date_input('Data Inicio', value=(datetime.today() - timedelta(days=30)))
data_fim = st.sidebar.date_input('Data Fim', value=datetime.today())


# pegamos precos de fechamento ajustados, ou seja, valores_iniciais = historico_precos[0] e valores finais =  historico_precos[1]
historico_precos = {acao: obter_precos(acao, data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')) for acao in carteira['Acoes']}

valores_iniciais = []
valores_finais = []


# Itera sobre as ações e qntd delas na carteira selecionada
for acao, qtd in zip(carteira['Acoes'], carteira['Quantidade']):

    valor_inicial = qtd * historico_precos[acao][0][1]
    valores_iniciais.append(valor_inicial)
    
    valor_final = qtd * historico_precos[acao][-1][1]
    valores_finais.append(valor_final)


valor_inicial_total = sum(valores_iniciais)
valor_final_total = sum(valores_finais)
rendimento_total = (valor_final_total - valor_inicial_total) / valor_inicial_total * 100

st.sidebar.write(f'Valor inicial: R$ {valor_inicial_total:.2f}')
st.sidebar.write(f'Valor final: R$ {valor_final_total:.2f}')
st.sidebar.write(f'Rendimento da carteira: {rendimento_total:.2f}%')


# ----- df
df_resumo = pd.DataFrame({
    'Acoes': carteira['Acoes'],
    'Quantidade': carteira['Quantidade'],
    'Valor Inicial Total R$': valores_iniciais,
    'Valor Final Total R$': valores_finais,
    'Rendimento %': [(final - inicial) / inicial * 100 for final, inicial in zip(valores_finais, valores_iniciais)]
})

# so p usuario selecionar graficos ou resumo
menu_opcoes = option_menu(
    menu_title=None,
    options=["Resumo", "Graficos"],
    default_index=0,
    orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "rgb(46, 134, 222)"}}  # cor fintz
)

st.title('Carteira de Acoes')

if menu_opcoes == 'Graficos':
    st.subheader('Distribuicao das Acoes na Carteira')
    fig, ax = plt.subplots()
    percentuais = [(valor / sum(valores_finais)) * 100 for valor in valores_finais]
    ax.pie(percentuais, labels=carteira['Acoes'], startangle=90, wedgeprops=dict(width=0.35))
    ax.axis('equal')
    st.pyplot(fig)

elif menu_opcoes == 'Resumo':
    st.subheader(f'Resumo das Acoes\n {data_inicio} - {data_fim}')
    st.dataframe(df_resumo)
