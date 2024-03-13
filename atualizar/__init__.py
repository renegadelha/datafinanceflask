import threading
import dataAnalise as da

def atualizarcorrInd3D(opcao):
    print('comecei')
    if opcao == 'all':
        da.gerarCorrelaAll('all').to_pickle('data/correlacoesIndAll3D.pkl')
    else:
        da.gerarCorrelaAll('minhas').to_pickle('data/correlacoesIndMinhas3D.pkl')
    print('terminei')

def atualizar():
    threading.Thread(target=atualizarcorrInd3D, args=("minhas",)).start()
