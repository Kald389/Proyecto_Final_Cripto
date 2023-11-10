import matplotlib.pyplot as plt
import mplfinance as mpf
from pykrakenapi import KrakenAPI
import krakenex

# Crear una instancia de la clase krakenex.API
api_krakenex = krakenex.API()

# Pasar la instancia de krakenex.API a KrakenAPI
api = KrakenAPI(api_krakenex)

# Obtener datos OHLC con una temporalidad de 1 hora
ohlc, last = api.get_ohlc_data("BTCUSD", interval=60)  # Intervalo de 60 minutos (1 hora)

# Invertir el orden de las filas en el DataFrame
ohlc = ohlc.iloc[::-1]

# Limpiar datos con NaN
ohlc_cleaned = ohlc.fillna(0)  # Reemplazar NaN con cero

# Crear un DataFrame compatible con el formato OHLC
ohlc_for_plot = ohlc_cleaned[['open', 'high', 'low', 'close', 'volume']]

# Graficar velas japonesas
mpf.plot(ohlc_for_plot, type='candle', volume=True, style='yahoo', title='Gráfico BTCUSD')
plt.show()
