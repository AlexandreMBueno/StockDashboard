''' Descricao -->
Endpoint que fornece os dados históricos de cotação dos ativos negociados na B3.
Formato OHLC (Open - High - Low - Close) para o ticker especificado e dentro do intervalo de datas determinado.
'''

import requests as req

# funcao para ler a chave de chave.txt

def ler_chave():
    with open('chave.txt', 'r') as file:
        for line in file:
            if line.startswith('chave_ab'):
                return line.split('=')[1].strip()
    return None

URL_BASE = 'https://api.fintz.com.br'
HEADERS = { 'X-API-Key': ler_chave() } # minha chave
PARAMS = { 'ticker': 'BBAS3', 'dataInicio': '2024-06-03'} # dataFim opcional

endpoint = URL_BASE + '/bolsa/b3/avista/cotacoes/historico'
res = req.get(endpoint, headers=HEADERS, params=PARAMS)
print(res.json())



# apenas dados precos de fechamento -->
# data = res.json()
# precos_fechamento = [item['precoFechamento'] for item in data]
# print(precos_fechamento)