import plotly.graph_objects as go

def gerarGrafRiscRet(df_final):
    fig = go.Figure(data=go.Scatter(x=df_final['ProbGanho'],
                              y=df_final['PercRetorno'],
                              mode='markers',
                              text=df_final.index))
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
