import pandas as pd
import yfinance as yf


def gerarcorrelacaoindividual(ticker, indicador):
    if indicador == 'selic':
        ind_df = consulta_bc(432)
    else:
        ind_df = consulta_bc(433)
    data_inicio = '2014-01-01'

    cotaMensal = yf.Ticker(ticker + ".SA").history(start=data_inicio).resample('M')['Close'].mean().to_frame()

    ind_df = ind_df[ind_df.index >= data_inicio]
    ind_df = ind_df.resample('M').mean()

    cotaMensal.drop(cotaMensal.tail(cotaMensal.size - ind_df.size).index, inplace=True)
    cotaMensal.index = cotaMensal.index.date
    ind_stock = pd.concat([ind_df, cotaMensal], axis=1, ignore_index=True)

    return round(float(ind_stock.corr().iloc(0)[1][0]), 3)


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

def getEmpresasListadasAntigas():
    return ['ABCB4', 'ABEV3', 'AGRO3', 'ALUP11', 'ARZZ3', 'B3SA3', 'BBAS3', 'BBDC4', 'BBSE3', 'BEEF3', 'BPAN4',
               'BRAP4', 'BRSR6', 'CAMB3', 'CCRO3', 'CIEL3', 'CMIG4', 'CPFE3', 'CPLE6', 'CSMG3', 'CSUD3', 'CYRE3',
               'DEXP3', 'EGIE3', 'ENGI11', 'EVEN3', 'FESA4', 'FLRY3', 'FRAS3', 'GGBR4', 'GOAU4', 'GRND3', 'HYPE3',
               'ITSA4', 'ITUB4', 'JHSF3', 'KEPL3', 'LEVE3', 'LREN3', 'MILS3', 'MULT3', 'ODPV3', 'PETR4', 'PINE4',
               'PNVL3', 'POMO4', 'POSI3', 'PSSA3', 'RANI3', 'RAPT4', 'RENT3', 'ROMI3', 'SANB11', 'SBSP3', 'SLCE3',
               'SMTO3', 'STBP3', 'TAEE11', 'TASA4', 'TGMA3', 'TIMS3', 'TOTS3', 'TRIS3', 'TRPL4', 'TUPY3', 'UGPA3',
               'UNIP6', 'VALE3', 'VIVT3', 'VLID3', 'VULC3', 'WEGE3']

def getMinhasEmpresasListadas():
    return ['BBSE3', 'PSSA3', 'BBAS3','BRSR6','ITSA4','EGIE3','ALUP11','TAEE11','KLBN4','VALE3', 'TUPY3','FESA4']