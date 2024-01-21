import dataAnalise as da
import json
import pandas as pd
import time
import yfinance as yf

s = time.time()
dados = da.calcularRiscoRetJanelasTemp()
print(time.time() - s)
print(dados)