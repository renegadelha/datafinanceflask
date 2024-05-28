import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pathlib
import pandas as pd
import dataAnalise as da

def dados_acao(nome):
    dados = yf.Ticker(nome + '.sa').history(start='2020-01-01')
    print(dados.columns)

    fig = px.line(dados, x=dados.index, y='Close')
    valor_acao = dados['Close'].iloc[-1]
    
    return fig.to_html(), valor_acao

def gerarBarGrafDividendos(data):

    fig = px.bar(data, x='ticker', y='mediana', hover_data=['valorDividendo', 'media'])
    return fig.to_html()

def gerarBarGrafAcao(data):

    fig = px.bar(data, x='ticker', y='mediana', hover_data=['ticker', 'media'])
    return fig.to_html()

def gerarGrafRiscRet(df_final):
    fig = go.Figure(data=go.Scatter(x=df_final['ProbGanho'],
                              y=df_final['PercRetorno'],
                              mode='markers',
                              text=df_final.index))
    fig.update_layout(
        xaxis_title= df_final.columns[0],
        yaxis_title= df_final.columns[1]

    )
    return fig.to_html()

def gerarGrafCorrIndicAll3D(df_final):
    fig = go.Figure(data=go.Scatter3d(x=df_final.iloc[:, 0],
                              y=df_final.iloc[:, 1],
                              z=df_final.iloc[:, 2],
                              mode='markers',
                              text=df_final.index),
                    )

    fig.update_layout(autosize=True,width=700,height=700 )
    fig.update_layout(
        scene=dict(
            xaxis_title=df_final.columns[0],
            yaxis_title=df_final.columns[1],
            zaxis_title=df_final.columns[2],
        )
    )
    return fig.to_html()

def gerarGrafCorrIndicAll(df_final):
    fig = go.Figure(data=go.Scatter(x=df_final.iloc[:, 0],
                              y=df_final.iloc[:, 1],
                              mode='markers',
                              text=df_final.index))

    fig.update_layout(autosize=True,width=900,height=500 )
    fig.update_layout(
        xaxis_title= df_final.columns[0],
        yaxis_title= df_final.columns[1]

    )
    return fig.to_html()


def gerarGrafCorrInd(graficodados, indicador):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name=indicador,
        x=graficodados.index,
        y=graficodados['indicador'],  # Dados para o eixo y,
        mode='lines',  # Tipo de gráfico: linhas,
        line=dict(color='blue')  # Altera a cor das linhas

    ))
    fig.update_layout(
        autosize=True,
        width=900,
        height=500
    )
    fig.add_trace(go.Scatter(
        name='Cotação',
        x=graficodados.index,
        y=graficodados['stock'],  # Dados para o eixo y,
        mode='lines',  # Tipo de gráfico: linhas,
        line=dict(color='red'),  # Altera a cor das linhas
        legendgroup='Cotação'
    ))
    return fig.to_html()

def pegar_maiores_empresas():
    actual_dir = pathlib.Path().absolute()
    path = f'{actual_dir}\\data\\statusinvest-busca-avancada.csv'
    path = path.split('datafinanceflask')[0] + 'datafinanceflask\\data\\statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados[dados['TICKER'].isin(da.pegar_listadas())]
    retorno = []
    #maior valor de mercado
    lista = dados.sort_values(by=[' VALOR DE MERCADO'], ascending=False)
    retorno.append(lista['TICKER'].head(6).values)

    #maior pagadora de dividendos
    lista = dados.sort_values(by=['DY'], ascending=False)
    retorno.append( lista['TICKER'].head(6).values)

    #menor relação preço/lucro
    lista = dados.sort_values(by=['P/L'], ascending=True)
    retorno.append( lista['TICKER'].head(6).values)

    #maior retorno de capital investido
    lista = dados.sort_values(by=['ROE'], ascending=False)
    retorno.append(lista['TICKER'].head(6).values)

    return retorno

def isListed(dados):
    listed = []
    for i in dados['TICKER']:
        if len(yf.Ticker(i + '.sa').history()) > 0:
            listed.append(i)

    return listed


def pegar_cotacao(tickers):
    tickers = [x + '.sa' for x in tickers]
    pares  = yf.download(tickers, period='1mo')['Adj Close'].ffill().iloc[-1]
    return pares.to_dict()


for tickers in pegar_maiores_empresas():
    print(tickers)
    print(pegar_cotacao(tickers))
    print('-------')



