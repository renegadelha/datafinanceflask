import dataAnalise as da
import json
import pandas as pd
import time
import yfinance as yf

dados = da.calcularRiscoRetJanelasTemp('minhas')
dados.to_pickle('data/riscoRetornoMinhas.pkl')
