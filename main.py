from flask import *
import dataAnalise as da
import grafico as gr
import atualizar
import dao
import carteira as gf

app = Flask(__name__)
app.secret_key = 'tem_que_definir_chave_secreta'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', default=None)
    return redirect('/login')

@app.route('/verificarlogin', methods=['POST','GET'])
def verificarlogin():
    if request.method == 'GET':
        user = 'rene@rene.com'
        senha = '123'
    else:
        user = request.form.get('user')
        senha = request.form.get('password')

    if dao.login(user, senha):
        session['user'] = user
        return render_template('logado.html', usuario=user)
    else:
        render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
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
    if request.method == 'GET':
        dataCorr = da.readCorrelacoesIndicFile('all')
    else:
        dataCorr = da.readCorrelacoesIndicFile('minhas')

    return render_template('correlationindicadores.html',
                           plot=gr.gerarGrafCorrIndicAll3D(dataCorr))

@app.route('/atualizarcorrelacaoindicadores')
def atualizarcorrelacaoallindicadores():
    atualizar.atualizar()
    return redirect('/correlacaoindicadores')

@app.route("/gerarminhacarteira") #decorator
def gerarminhacarteira():
    data, grid = gf.gerarPercentuais()
    lista = [['ticker', 'percentual']]
    for key, val in data.items():
        lista.append([key, val])

    return render_template('minhacarteira.html', data=lista, grid=grid)

@app.route('/rankingdividendos/<opcao>', methods=['GET','POST'])
def gerarrankingdividendos(opcao):
    if opcao == 'all':
        data = da.readRankingDividendos('all').head(40)
    else:
        data = da.readRankingDividendos('minhas')

    return render_template('rankingdividendos.html', plot=gr.gerarBarGrafDividendos(data))


if __name__ == "__main__":
    app.run(debug=True)