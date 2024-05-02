import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

btc = yf.download('BTC-USD', start='2024-03-13', end=datetime.today().strftime('%Y-%m-%d'))

SMA = int(input("rentrez la valeur de vla moyenne mobile : ")) #choisir une sma inférieur à l'intervalle entre start et end

btc['SMA'] = btc['Close'].rolling(window=SMA).mean()

# Detecting crossovers
btc['Position'] = np.where(btc['Close'] > btc['SMA'], 1, -1)
btc['Crossover'] = btc['Position'].diff()

# plt.figure(figsize=(10, 5))
plt.plot(btc['Close'])
plt.plot(btc['SMA'], label='SMA', color='red')
# plt.title('Bitcoin Closing Price')
# plt.xlabel('Date')
# plt.ylabel('Price in USD')
# plt.grid(False)
# plt.show()

print("position and crossover",btc['Position'], btc['Crossover'])

print("index",btc[btc['Crossover'] == 2].index)

# Highlight buy signals
plt.plot(btc[btc['Crossover'] == 2].index, btc['SMA'][btc['Crossover'] == 2], '^', markersize=10, color='green', lw=0, label='Buy Signal')

# Highlight sell signals
plt.plot(btc[btc['Crossover'] == -2].index, btc['SMA'][btc['Crossover'] == -2], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

plt.title('Bitcoin Closing Price, SMA, and Crossover Signals')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.legend()
plt.grid(True)
plt.show()

print("crossSMA +", btc['SMA'][btc['Crossover'] == 2])
print("crossSMA -", btc['SMA'][btc['Crossover'] == -2])
print("cross", [btc['Crossover']])

# pf = portefeuille
pf = int(input("rentrez la valeur de votre portefeuille : "))

btc_held = 0

portfolio_values = []
date = []

# Itération sur chaque ligne du DataFrame pour appliquer la logique d'achat et de vente
for idx, row in btc.iterrows():
    if row['Crossover'] == 2:  # Signal d'achat
        print(row['Close'])
        btc_held = pf / row['SMA']
        pf = 0
        portfolio_values.append(btc_held * row['SMA']) #ici on assigne portfolio value au prix du bitcoin en dollars, on utilise cette même logique pour vendre 3 ligne après, mais ici on va juste faire la conversion pour visualiser la valeur de btc en dollars
        date.append(idx)
    elif row['Crossover'] == -2:  # Signal de vente
        print(row['Close'])
        pf = btc_held * row['SMA']
        btc_held = 0
        portfolio_values.append(pf) #ici on a pas besoin de convertir, c'est fais deux ligne au dessus
        date.append(idx)


# Affichage de la valeur finale du portefeuille
print(f"Valeur finale du portefeuille: ${pf:.2f}")
   
plt.plot(date, portfolio_values, marker='o', linestyle='-', color='b')
plt.title('Évolution de la Valeur du Portefeuille')
plt.xlabel('Date')
plt.ylabel('Valeur du Portefeuille ($)')

plt.grid(True)
plt.show()