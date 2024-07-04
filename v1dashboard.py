import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as pyplot
import altair as alt

# line chart

st.title('Line chart')
data = pd.DataFrame(np.random.rand(12, 1,), columns=['a'])
st.line_chart(data)

#rand(12, 1) gera um array de numeros aleatorios com 12 linhas e 1 coluna
# se quiser colocar mais colunas, ou seja, linhas no grafico, precisamos tambem adicionar a coluna desejada em columns = ['b'] por ex

# map

st.title("Map")
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [49.28, -123.12], # 100 pontos de coordenadas proximas a [49.28, -123.12]
    columns=['lat', 'lon']) # 50 50 --> dividi cada valor do array por 50 para os pontos ficarem mais concentrados ao redor da cord.
st.map(map_data)






# Stock line chart

st.title('Stock Line chart')


dados = {
    'Mes': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10', '2024-01-11', '2024-01-12'],
    'Valor': ['15.0', '20.2', '16.5', '17.4', '17.5', '18.5', '19.0', '17.8', '20.0', '16.5', '19.2', '18.8']
}

df = pd.DataFrame(dados)
df['Valor'] = df['Valor'].astype(float)
print(df['Mes'].dtypes)
df['Mes'] = pd.Categorical(df['Mes'], categories=['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04',
                                                   '2024-01-05', '2024-01-06', '2024-01-07', '2024-01-08',
                                                     '2024-01-09', '2024-01-10', '2024-01-11', '2024-01-12'],
                                                     ordered=True)
print(df['Mes'].dtypes)
st.line_chart(df.set_index('Mes'))
