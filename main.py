import streamlit as st
import matplotlib.pyplot as plt
import mplfinance as mpf
from pykrakenapi import KrakenAPI
import krakenex
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class CryptoChart:
    def __init__(self):
        # Crear una instancia de la clase krakenex.API
        self.api_krakenex = krakenex.API()
        # Pasar la instancia de krakenex.API a KrakenAPI
        self.api = KrakenAPI(self.api_krakenex)

    def get_ohlc_data(self, pair, timeframe, lookback_days=90):
        # Mapeo de las temporalidades a sus equivalentes en minutos
        timeframe_mapping = {
            "1D": 1440,  # 1 día en minutos
            "4H": 240,   # 4 horas en minutos
            "1H": 60,    # 1 hora en minutos
            "1W": 10080  # 1 semana en minutos
        }

        try:
            interval = timeframe_mapping.get(timeframe, 60)  # Valor predeterminado: 60 minutos

            # Obtener la fecha actual
            end_date = datetime.now()

            # Calcular la fecha de inicio restando el número de días de la mirada hacia atrás
            start_date = end_date - timedelta(days=lookback_days)

            # Obtener datos OHLC para el par seleccionado y el rango de fechas
            ohlc, last = self.api.get_ohlc_data(pair, interval=interval, since=start_date.timestamp())
            ohlc = ohlc.iloc[::-1]
            ohlc_cleaned = ohlc.fillna(0)
            ohlc_for_plot = ohlc_cleaned[['open', 'high', 'low', 'close', 'volume']]

            return ohlc_for_plot
        except Exception as e:
            st.error(f"Error al obtener datos para el par {pair}: {e}")
            return None

    def calculate_stochastic(self, ohlc_data, window=14):
        # Calcular %K
        high_max = np.maximum.accumulate(ohlc_data['high'].values)
        low_min = np.minimum.accumulate(ohlc_data['low'].values)
        ohlc_data['%K'] = 100 * ((ohlc_data['close'].values - low_min) / (high_max - low_min))

        # Calcular %D (media móvil de %K)
        ohlc_data['%D'] = ohlc_data['%K'].rolling(window=window).mean()

        return ohlc_data


    def plot_candlestick_chart(self, ohlc_data, selected_pair, selected_timeframe):
        # Calcular el estocástico
        ohlc_data = self.calculate_stochastic(ohlc_data)

        # Crear una figura
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3, 1, 1]}, sharex=True, figsize=(10, 8))

        # Agregar labels gráfica principal
        ax1.set_xlabel('Precio en USDT')

        # Graficar velas japonesas en el primer eje
        mpf.plot(ohlc_data, type='candle', style='yahoo', ax=ax1, show_nontrading=True, ylabel='left')

        # Ajustes de diseño para el gráfico de velas
        ax1.yaxis.tick_left()  # Mover ticks del eje y a la izquierda
        ax1.xaxis.set_major_locator(plt.MaxNLocator(6))  # Mostrar hasta 6 fechas en el eje x

        # Graficar volumen en el segundo eje
        ax2.fill_between(ohlc_data.index, ohlc_data['volume'], color='gray', alpha=0.5)
        ax2.set_ylabel('Volumen')

        # Ajustes de diseño para el gráfico de volumen
        ax2.yaxis.tick_left()  # Mover ticks del eje y a la izquierda
        ax2.xaxis.set_major_locator(plt.MaxNLocator(6))  # Mostrar hasta 6 fechas en el eje x

        # Graficar estocástico en el tercer eje
        ax3.plot(ohlc_data.index, ohlc_data['%K'], label='Standard Stochastic', color='blue')
        ax3.plot(ohlc_data.index, ohlc_data['%D'], label='MA Stochastic', color='orange')
        ax3.axhline(80, color='red', linestyle='--', label='Overbought (80)')
        ax3.axhline(20, color='green', linestyle='--', label='Oversold (20)')

        # Ajustes de diseño para el gráfico de estocástico
        ax3.set_xlabel('Fecha')
        ax3.set_ylabel('Estocástico')
        ax3.legend(loc='upper left')

        # Ajustes generales
        fig.suptitle(f'Gráfico {selected_pair} - Temporalidad {selected_timeframe}', fontsize=16)

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)
def main():
    crypto_chart = CryptoChart()

    # Lista de pares específicos
    selected_pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "ATOMUSDT", "DOGEUSDT", "ROSEUSDT", "SOLUSDT", "MATICUSDT", "HBARUSDT"]

    # Seleccionar par mediante un widget de Streamlit
    selected_pair = st.selectbox('Selecciona un par de criptomonedas:', selected_pairs)

    # Lista de temporalidades
    selected_timeframes = ["1W", "1D", "4H", "1H"]

    # Seleccionar temporalidad mediante un widget de Streamlit
    selected_timeframe = st.selectbox('Selecciona la temporalidad:', selected_timeframes)

    # Obtener datos OHLC para el par seleccionado y la temporalidad seleccionada
    ohlc_data = crypto_chart.get_ohlc_data(selected_pair, selected_timeframe)

    if ohlc_data is not None:
        crypto_chart.plot_candlestick_chart(ohlc_data, selected_pair, selected_timeframe)

if __name__ == "__main__":
    main()
