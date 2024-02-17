from flask import *
import dataAnalise as da
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('home.html')

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

@app.route('/correlacaoindividual', methods=['POST','GET'])
def correlacaotickerindicador():
    if request.method == 'POST':
        indicador = request.form.get('indicador_radio')
        ticker = str(request.form.get('ticker'))

        correlacao = da.gerarcorrelacaoindividual(ticker, indicador)

        return render_template('correlationindicador.html', correlac=correlacao)

    else:
        return render_template('correlationindicador.html')



if __name__ == "__main__":
    app.run(debug=True)