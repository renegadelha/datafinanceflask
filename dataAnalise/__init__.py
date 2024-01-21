import pandas as pd
import yfinance as yf
import json

def calcularRiscoRetJanelasTemp():

    comps = list(pd.read_json('data/minhasEmpresas.json').to_dict()[0].values())
    dataProbGanho = pd.DataFrame()
    dataPerctRetorno = pd.DataFrame()


    for comp in comps:
        saida = gerarDataRetornos(comp)
        dataProbGanho = pd.concat([dataProbGanho, pd.DataFrame([[comp, saida['percGanhos'].values[0]]])])
        dataPerctRetorno = pd.concat([dataPerctRetorno, pd.DataFrame([[comp, saida['Rentb'].values[0]]])])

    dataProbGanho.columns = ['ticker', 'ProbGanho']
    dataPerctRetorno.columns = ['ticker', 'PercRetorno']

    df_final = dataProbGanho.merge(dataPerctRetorno, how='left', on='ticker')
    df_final.set_index('ticker', inplace=True)

    return df_final


def calcRetorno(week, janela):

    retW = (week / week.shift(janela) - 1) * 100

    retW.dropna(inplace=True)
    totalJanelas = len(retW)

    qtdeJanPosit = len(retW[retW['Adj Close'] > 0])
    return [(qtdeJanPosit / totalJanelas) * 100 - 100, retW['Adj Close'].mean()]


def gerarDataRetornos(ticker):
    probGanhos = list()
    rentMedia = list()

    intervalo = 4
    maxSemanas = 192

    hist = yf.download(ticker, start='2014-01-01')
    week = hist.resample('W').mean()

    for i in range(48, maxSemanas, intervalo):
        saida = calcRetorno(week, i)
        probGanhos.append(saida[0])
        rentMedia.append(saida[1])

    data = pd.DataFrame(list(zip(list([*range(4, maxSemanas, intervalo)]), probGanhos, rentMedia)),
                        columns=['interv', 'percGanhos', 'Rentb'])
    data = data.set_index('interv')
    return data[-1:]