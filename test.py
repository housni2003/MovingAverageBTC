import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

btc = yf.download('BTC-USD', start='2024-03-13', end=datetime.today().strftime('%Y-%m-%d')) 

portfolio_values = {}

for i in range(1, 30):

    btc['SMA'] = btc['Close'].rolling(window=i).mean()

    # Detecting crossovers
    btc['Position'] = np.where(btc['Close'] > btc['SMA'], 1, -1)
    btc['Crossover'] = btc['Position'].diff()

    # # plt.figure(figsize=(10, 5))
    # plt.plot(btc['Close'])
    # plt.plot(btc['SMA'], label='SMA', color='red')
    # # plt.title('Bitcoin Closing Price')
    # # plt.xlabel('Date')
    # # plt.ylabel('Price in USD')
    # # plt.grid(False)
    # # plt.show()

    # print("position and crossover",btc['Position'], btc['Crossover'])

    # print("index",btc[btc['Crossover'] == 2].index)

    # # Highlight buy signals
    # plt.plot(btc[btc['Crossover'] == 2].index, btc['SMA'][btc['Crossover'] == 2], '^', markersize=10, color='green', lw=0, label='Buy Signal')

    # # Highlight sell signals
    # plt.plot(btc[btc['Crossover'] == -2].index, btc['SMA'][btc['Crossover'] == -2], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

    # plt.title('Bitcoin Closing Price, SMA, and Crossover Signals')
    # plt.xlabel('Date')
    # plt.ylabel('Price in USD')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # print("crossSMA +", btc['SMA'][btc['Crossover'] == 2])
    # print("crossSMA -", btc['SMA'][btc['Crossover'] == -2])
    # print("cross", [btc['Crossover']])

    # pf = portefeuille
    pf = 2000

    btc_held = 0

    # Itération sur chaque ligne du DataFrame pour appliquer la logique d'achat et de vente
    for idx, row in btc.iterrows():
        if row['Crossover'] == 2:  # Signal d'achat
            print(row['Close'])
            btc_held = pf / row['SMA']
            pf = 0
        elif row['Crossover'] == -2:  # Signal de vente
            print(row['Close'])
            pf = btc_held * row['SMA']
            btc_held = 0
    portfolio_values[i] = pf
    # Affichage de la valeur finale du portefeuille
    print(f"Valeur finale du portefeuille: ${pf:.2f}")
# Trouver la période de SMA qui maximise la valeur du portefeuille
best_sma_period = max(portfolio_values, key=portfolio_values.get)
best_portfolio_value = portfolio_values[best_sma_period]

print(f"La meilleure période SMA est {best_sma_period} jours avec un portefeuille final de ${best_portfolio_value:.2f}")

# Création du graphique
sma_periods = list(portfolio_values.keys())
final_values = list(portfolio_values.values())

plt.figure(figsize=(10, 6))
plt.bar(sma_periods, final_values, color='blue')
plt.xlabel('Période de la SMA (jours)')
plt.ylabel('Valeur finale du portefeuille ($)')
plt.title('Valeur finale du portefeuille en fonction de la période SMA')
plt.xticks(sma_periods)  # Assure que tous les labels de période sont affichés
plt.grid(True)
plt.show()