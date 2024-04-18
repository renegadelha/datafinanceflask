import psycopg2

def conectardb():
    con = psycopg2.connect(
        host='localhost',
    database = 'datafinanceflask',
        user = 'postgres',
    password = '123'
    )

    return con

@app.route('/login', methods=['POST'])
def data():
    nome = request.form['nome']
    profissao = request.form['profissao']
    estado = request.form['estado']
    email = request.form['email']
    senha = request.form['senha']
    
    con = conectardb()
    cur = con.cursor()

    cur.execute("INSERT INTO usuarios (nome, email, estado, profissao, senha) VALUES (%s, %s, %s, %s, %s)", (nome, email, estado, profissao, senha))
    
    con.commit()
    cur.close()
    con.close()

    return redirect('/login')

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

def getCarteira():
    return {'SIMH3':30, 'TAEE11':6, 'ALUP11':13, 'EGIE3':8, 'KLBN11':11, 'ITSA4':30,
             'PSSA3':7, 'BBSE3':9, 'VBBR3':13, 'BRSR6':22, 'TUPY3':6, 'BBAS3':6, 'VALE3':3}



resp = login('rene@rene.com','12345')
print(resp)
