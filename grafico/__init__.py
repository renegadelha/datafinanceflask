import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pathlib
import pandas as pd

def dados_acao(nome):
    dados = yf.Ticker(nome + '.sa').history(start='2020-01-01')
    print(dados.columns)

    fig = px.line(dados, x=dados.index, y='Close')
    valor_acao = dados['Close'].iloc[-1]
    
    return fig.to_html(), valor_acao

    

def gerarBarGrafDividendos(data):

    fig = px.bar(data, x='ticker', y='mediana', hover_data=['valorDividendo', 'media'])
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
    lista = dados.sort_values(by=[' VALOR DE MERCADO'], ascending=False)
    return lista[['TICKER', ' VALOR DE MERCADO', 'PRECO']].head(50)

print(pegar_maiores_empresas())

#def pegar_dados_via_Yfinance(nome):
    #tick = yf.Ticker(nome + '.SA')
    #info = tick.info
    #for key, value in info.items():
        #print(f"{key}: {value}")

#pegar_dados_via_Yfinance('PETR4')
