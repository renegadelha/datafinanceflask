from flask import *
import dataAnalise as da
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcularRiscoRetorno/<opcao>', methods=['GET','POST'])
def calcularRiscoRetorno(opcao):
    df_final = da.readRiscoRetornoFile(opcao)
    fig = go.Figure(data=go.Scatter(x=df_final['ProbGanho'],
                              y=df_final['PercRetorno'],
                              mode='markers',
                              text=df_final.index))
    return render_template('calcRiscoRet.html', plot=fig.to_html())



if __name__ == "__main__":
    app.run(debug=True)