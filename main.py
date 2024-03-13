from flask import *
import dataAnalise as da
import grafico as gr


app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/teste')
def teste():
    return render_template('./hometeste.html')

@app.route('/')
def home():
    return render_template('./home2.html')

#@app.route('/')
#def home2():
#    return render_template('./home.html')

@app.route('/testes')
def testes():
    return render_template('./testes.html')

@app.route('/antiga')
def homeantiga():
    return render_template('index.html')


@app.route('/calcularRiscoRetorno/<opcao>', methods=['GET','POST'])
def calcularRiscoRetorno(opcao):
    df_final = da.readRiscoRetornoFile(opcao)
    return render_template('calcRiscoRet.html', plot=gr.gerarGrafRiscRet(df_final))

@app.route('/correlacaoindividual', methods=['POST','GET'])
def correlacaotickerindicador():
    if request.method == 'POST':
        indicador = request.form.get('indicador_radio')
        ticker = str(request.form.get('ticker'))

        correlacao, graficodados = da.gerarcorrelacaoindividual(ticker, indicador)
        return render_template('correlationindicador.html', correlac=correlacao, plot=gr.gerarGrafCorrInd(graficodados,indicador))

    else:
        return render_template('correlationindicador.html')

@app.route('/correlacaoindicadores', methods=['POST','GET'])
def correlacaoallindicadores():
    dataCorr = da.readCorrelacoesIndicFile('minhas')

    return render_template('correlationindicadores.html',
                           plot=gr.gerarGrafCorrIndicAll3D(dataCorr))


if __name__ == "__main__":
    app.run(debug=True)