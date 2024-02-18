import pandas as pd
import numpy as np
import yfinance as yf
from dao import *


def gerarrankingdividendos(dados):
    dataf = []
    for empresa in dados:
        data = dyanalise(empresa)
        if 0 != data:
            dataf.append(data)

    df = pd.DataFrame(np.array(dataf), columns=['ticker', 'valorDividendo', 'mediana', 'media'])
    df = df.astype({"ticker": str, "valorDividendo": float, "mediana": float, "media": float})
    df.drop(df[df['mediana'] < 1].index, inplace=True)

    df = df.sort_values(by=['mediana'], ascending=False)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    return df

def dyanalise(name):
    empresa = name + '.SA'
    comp = yf.Ticker(empresa)
    hist2 = comp.history(start='2013-01-01')
    if (len(hist2) == 0):
        return 0
    somaDiv = hist2['Dividends'].resample('Y').sum()
    meanPrice = hist2['Close'].resample('Y').median()
    result = somaDiv / meanPrice * 100

    return [name, float("{0:.2f}".format(somaDiv.median())), float("{0:.2f}".format(result.median())), float("{0:.2f}".format(result.mean()))]

def gerarcorrelacaoindividual(ticker, indicador):
    if indicador == 'selic':
        ind_df = consulta_bc(432)
    elif indicador == 'ibcbr':
        ind_df = consulta_bc(24364)
    elif indicador == 'ipca':
        ind_df = consulta_bc(433)
    data_inicio = '2014-01-01'

    cotaMensal = yf.Ticker(ticker + ".SA").history(start=data_inicio).resample('M')['Close'].mean().to_frame()

    ind_df = ind_df[ind_df.index >= data_inicio]
    ind_df = ind_df.resample('M').mean()


    if cotaMensal.size - ind_df.size > 0:
        cotaMensal.drop(cotaMensal.tail(cotaMensal.size - ind_df.size).index, inplace=True)

    cotaMensal.index = pd.to_datetime(cotaMensal.index.date)

    ind_stock = pd.concat([ind_df, cotaMensal], axis=1, ignore_index=True)
    df_norm = (ind_stock - ind_stock.min()) / (ind_stock.max() - ind_stock.min())
    df_norm.columns = ['indicador', 'stock']

    return round(float(df_norm.corr().iloc(0)[1][0]), 3), df_norm


#https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
def consulta_bc(codigo_bcb):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
    df = pd.read_json(url)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df.set_index('data', inplace=True)
    return df



def readRiscoRetornoFile(opcao):
    if opcao == 'all':
        return pd.read_pickle('data/riscoRetornoAll.pkl')
    else:
        return pd.read_pickle('data/riscoRetornoMinhas.pkl')

def readCorrelacoesIndicFile(opcao):
    if opcao == 'all':
        return pd.read_pickle('data/correlacoesIndAll3D.pkl')
    else:
        return pd.read_pickle('data/correlacoesIndMinhas3D.pkl')

def readRankingDividendos(opcao):
    if opcao == 'all':
        return pd.read_pickle('data/rankingdividendosAll.pkl')
    else:
        return pd.read_pickle('data/rankingdividendosMinhas.pkl')


def gerarCorrelaAll(opcao):

    if opcao == 'all':
        tickers = getEmpresasListadasAntigas()
    else:
        tickers = getMinhasEmpresasListadas()

    lista = []
    for ticker in tickers:
        ipca = gerarcorrelacaoindividual(ticker ,'ipca')
        selic = gerarcorrelacaoindividual(ticker , 'selic')
        ibcbr = gerarcorrelacaoindividual(ticker, 'ibcbr')

        lista.append([ipca[0], selic[0], ibcbr[0]])

    data = pd.DataFrame(lista, index=tickers,columns=['ipca','selic','ibcbr'])
    return data



def calcularRiscoRetJanelasTemp(opcao):

    if opcao == 'all':
        tickers = getEmpresasListadasAntigas()
    else:
        tickers = getMinhasEmpresasListadas()

    comps = [x + '.sa' for x in tickers]

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
    return [abs((qtdeJanPosit / totalJanelas) * 100 - 100), retW['Adj Close'].mean()]


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
