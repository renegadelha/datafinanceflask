import dataAnalise as da
import json
import pandas as pd
import time
import yfinance as yf

#dados = da.calcularRiscoRetJanelasTemp('minhas')
#dados.to_pickle('data/riscoRetornoMinhas.pkl')

#dados = da.gerarcorrelacaoindividual('bbas3', 'selic')
#print(dados[0])

da.gerarCorrelaAll('all').to_pickle('data/correlacoesIndAll3D.pkl')

