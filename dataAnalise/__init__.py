import pandas as pd
import numpy as np
import yfinance as yf
from dao import *

def pegarcotacoes():
    nomesAcoes = ['bbas3.sa', 'itsa4.sa','brsr6.sa','egie3.sa','alup11.sa', 'abcb4.sa']

    dados = yf.download(nomesAcoes)
    valores = [round(x, 2) for x in list(dados['Adj Close'].ffill().iloc[-1].values)]
    nomes = [y.replace('.SA', '') for y in list(dados['Adj Close'].columns.values)]

    pares = []
    for i in range(len(nomes)):
        pares.append([nomes[i], valores[i]])

    return pares

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
    hist2 = comp.history(period='15y')
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
    #normalizaçao dos dados
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

    hist = yf.download(ticker, period='15y')
    week = hist.resample('W').mean()

    for i in range(48, maxSemanas, intervalo):
        saida = calcRetorno(week, i)
        probGanhos.append(saida[0])
        rentMedia.append(saida[1])

    data = pd.DataFrame(list(zip(list([*range(4, maxSemanas, intervalo)]), probGanhos, rentMedia)),
                        columns=['interv', 'percGanhos', 'Rentb'])
    data = data.set_index('interv')
    return data[-1:]

def gerar_top_acoes(tipo):
    dados = pd.read_csv('data//statusinvest-busca-avancada.csv', decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)

    dados.drop(dados[dados[' LIQUIDEZ MEDIA DIARIA'] < 1000000].index, inplace=True)
    dados.drop(dados[dados['P/L'] <= 0].index, inplace=True)
    dados.drop(dados[dados[' LPA'] <= 0].index, inplace=True)
    dados.drop(dados[dados['EV/EBIT'] <= 0].index, inplace=True)
    dados.drop(dados[dados['EV/EBIT'] > 30].index, inplace=True)
    dados.drop(dados[dados['PRECO'] <= 0].index, inplace=True)

    print(dados.columns)

def pegar_listadas():

    return ['AALR3', 'ABCB4', 'ABEV3', 'ADHM3', 'AERI3', 'AESB3', 'AFLT3', 'AGRO3', 'AGXY3', 'AHEB3', 'AHEB5', 'AHEB6', 'ALLD3', 
            'ALOS3', 'ALPA3', 'ALPA4', 'ALPK3', 'ALUP11', 'ALUP3', 'ALUP4', 'AMAR3', 'AMBP3', 'AMER3', 'ANIM3', 'APER3', 'ARML3', 
            'ARZZ3', 'ASAI3', 'ATMP3', 'ATOM3', 'AURA33', 'AURE3', 'AVLL3', 'AZEV3', 'AZEV4', 'AZUL4', 'B3SA3', 'BAHI3', 'BALM3', 
            'BALM4', 'BAUH4', 'BAZA3', 'BBAS3', 'BBDC3', 'BBDC4', 'BBSE3', 'BDLL3', 'BDLL4', 'BEEF3', 'BEES3', 'BEES4', 'BGIP3', 
            'BGIP4', 'BHIA3', 'BIOM3', 'BLAU3', 'BMEB3', 'BMEB4', 'BMGB4', 'BMIN3', 'BMIN4', 'BMKS3', 'BMOB3', 'BNBR3', 'BOBR3', 'BOBR4', 'BPAC11', 'BPAC3', 'BPAC5', 'BPAN4', 'BPHA3', 'BRAP3', 'BRAP4', 'BRBI11', 'BRFS3', 'BRGE11', 'BRGE12', 'BRGE3', 'BRGE5', 'BRGE6', 'BRGE7', 'BRGE8', 'BRIT3', 'BRIV3', 'BRIV4', 'BRKM3', 'BRKM5', 'BRKM6', 'BRPR3', 'BRSR3', 'BRSR5', 'BRSR6', 'BSLI3', 'BSLI4', 'CALI3', 'CAMB3', 'CAML3', 'CASH3', 'CASN3', 'CASN4', 'CBAV3', 'CBEE3', 'CCRO3', 'CEAB3', 'CEBR3', 'CEBR5', 'CEBR6', 'CEDO3', 'CEDO4', 'CEEB3', 'CEEB5', 'CEED3', 'CEED4', 'CEGR3', 'CGAS3', 'CGAS5', 'CGRA3', 'CGRA4', 'CIEL3', 'CLSA3', 'CLSC3', 'CLSC4', 'CMIG3', 'CMIG4', 'CMIN3', 'COCE3', 'COCE5', 'COCE6', 'COGN3', 'CORR3', 'CORR4', 'CPFE3', 'CPLE3', 'CPLE5', 'CPLE6', 'CRFB3', 'CRIV3', 'CRIV4', 'CRPG3', 'CRPG5', 'CRPG6', 'CSAN3', 'CSED3', 'CSMG3', 'CSNA3', 'CSRN3', 'CSRN5', 'CSRN6', 'CSUD3', 'CTKA3', 'CTKA4', 'CTNM3', 'CTNM4', 'CTSA3', 'CTSA4', 'CURY3', 'CVCB3', 'CXSE3', 'CYRE3', 'DASA3', 'DESK3', 'DEXP3', 'DEXP4', 'DIRR3', 'DMVF3', 'DOHL3', 'DOHL4', 'DOTZ3', 'DTCY3', 'DXCO3', 'EALT3', 'EALT4', 'ECOR3', 'ECPR3', 'ECPR4', 'EGIE3', 'EKTR3', 'EKTR4', 'ELET3', 'ELET5', 'ELET6', 'ELMD3', 'EMAE3', 'EMAE4', 'EMBR3', 'ENAT3', 'ENEV3', 'ENGI11', 'ENGI3', 'ENGI4', 'ENJU3', 'ENMT3', 'ENMT4', 'EPAR3', 'EQPA3', 'EQPA5', 'EQPA6', 'EQPA7', 'EQTL3', 'ESPA3', 'ESTR3', 'ESTR4', 'ETER3', 'EUCA3', 'EUCA4', 'EVEN3', 'EZTC3', 'FESA3', 'FESA4', 'FHER3', 'FIEI3', 'FIGE3', 'FIGE4', 'FIQE3', 'FLRY3', 'FRAS3', 'FRIO3', 'FRTA3', 'G2DI33', 'GEPA3', 'GEPA4', 'GFSA3', 'GGBR3', 'GGBR4', 'GGPS3', 'GMAT3', 'GOAU3', 'GOAU4', 'GOLL4', 'GPAR3', 'GPIV33', 'GRND3', 'GSHP3', 'GUAR3', 'HAGA3', 'HAGA4', 'HAPV3', 'HBOR3', 'HBRE3', 'HBSA3', 'HBTS5', 'HETA3', 'HETA4', 'HOOT3', 'HOOT4', 'HYPE3', 'IFCM3', 'IGTI11', 'IGTI3', 'IGTI4', 'INEP3', 'INEP4', 'INTB3', 'IRBR3', 'ITSA3', 'ITSA4', 'ITUB3', 'ITUB4', 'JALL3', 'JBSS3', 'JFEN3', 'JHSF3', 'JOPA3', 'JOPA4', 'JSLG3', 'KEPL3', 'KLBN11', 'KLBN3', 'KLBN4', 'KRSA3', 'LAND3', 'LAVV3', 'LEVE3', 'LIGT3', 'LIPR3', 'LJQQ3', 'LOGG3', 'LOGN3', 'LPSB3', 'LREN3', 'LUPA3', 'LUXM3', 'LUXM4', 'LVTC3', 'LWSA3', 'MAPT3', 'MAPT4', 'MATD3', 'MBLY3', 'MDIA3', 'MDNE3', 'MEAL3', 'MELK3', 'MERC3', 'MERC4', 'MGEL3', 'MGEL4', 'MGLU3', 'MILS3', 'MLAS3', 'MMAQ3', 'MMAQ4', 'MNDL3', 'MNPR3', 'MOAR3', 'MOVI3', 'MRFG3', 'MRSA3B', 'MRSA5B', 'MRSA6B', 'MRVE3', 'MSPA3', 'MSPA4', 'MTRE3', 'MTSA3', 'MTSA4', 'MULT3', 'MWET3', 'MWET4', 'MYPK3', 'NEMO3', 'NEOE3', 'NEXP3', 'NGRD3', 'NINJ3', 'NORD3', 'NTCO3', 'NUTR3', 'ODER4', 'ODPV3', 'OFSA3', 'OIBR3', 'OIBR4', 'ONCO3', 'OPCT3', 'ORVR3', 'OSXB3', 'PATI3', 'PATI4', 'PCAR3', 'PDGR3', 'PDTC3', 'PEAB3', 'PEAB4', 'PETR3', 'PETR4', 'PETZ3', 'PFRM3', 'PGMN3', 'PINE3', 'PINE4', 'PLAS3', 'PLPL3', 'PMAM3', 'PNVL3', 'POMO3', 'POMO4', 'PORT3', 'POSI3', 'PPAR3', 'PPLA11', 'PRIO3', 'PRNR3', 'PSSA3', 'PTBL3', 'PTNT3', 'PTNT4', 'QUAL3', 'RADL3', 'RAIL3', 'RAIZ4', 'RANI3', 'RAPT3', 'RAPT4', 'RCSL3', 'RCSL4', 'RDNI3', 'RDOR3', 'RECV3', 'REDE3', 'RENT3', 'RNEW11', 'RNEW3', 'RNEW4', 'ROMI3', 'RPAD3', 'RPAD5', 'RPAD6', 'RPMG3', 'RRRP3', 'RSID3', 'RSUL3', 'RSUL4', 'SANB11', 'SANB3', 'SANB4', 'SAPR11', 'SAPR3', 'SAPR4', 'SBFG3', 'SBSP3', 'SCAR3', 'SEER3', 'SEQL3', 'SGPS3', 'SHOW3', 'SHUL3', 'SHUL4', 'SIMH3', 'SLCE3', 'SLED3', 'SLED4', 'SMFT3', 'SMTO3', 'SNSY3', 'SNSY5', 'SNSY6', 'SOJA3', 'SOMA3', 'SOND3', 'SOND5', 'SOND6', 'SRNA3', 'STBP3', 'SUZB3', 'SYNE3', 'TAEE11', 'TAEE3', 'TAEE4', 'TASA3', 'TASA4', 'TCSA3', 'TECN3', 'TEKA3', 'TEKA4', 'TELB3', 'TELB4', 'TEND3', 'TFCO4', 'TGMA3', 'TIMS3', 'TKNO3', 'TKNO4', 'TOTS3', 'TPIS3', 'TRAD3', 'TRIS3', 'TRPL3', 'TRPL4', 'TTEN3', 'TUPY3', 'TXRX3', 'TXRX4', 'UCAS3', 'UGPA3', 'UNIP3', 'UNIP5', 'UNIP6', 'USIM3', 'USIM5', 'USIM6', 'VALE3', 'VAMO3', 'VBBR3', 'VITT3', 'VIVA3', 'VIVR3', 'VIVT3', 'VLID3', 'VSPT3', 'VSTE3', 'VULC3', 'VVEO3', 'WEGE3', 'WEST3', 'WHRL3', 'WHRL4', 'WIZC3', 'WLMM3', 'WLMM4', 'YDUQ3', 'ZAMP3']
