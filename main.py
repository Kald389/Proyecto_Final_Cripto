import streamlit as st
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
from pykrakenapi import KrakenAPI
import krakenex
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

class CryptoChart:
    def __init__(self):
        self.api_krakenex = krakenex.API()
        self.api = KrakenAPI(self.api_krakenex)

    def get_lookback_days(self, selected_timeframe):
        if selected_timeframe == "1D":
            return 90
        elif selected_timeframe == "1W":
            return 365 * 2
        elif selected_timeframe == "4H":
            return 30  # Cambiado a 30 días para incluir más velas de 4H
        elif selected_timeframe == "1H":
            return 10   # Cambiado a 7 días para incluir más velas de 1H
        else:
            return 90

    def get_ohlc_data(self, pair, timeframe):
        timeframe_mapping = {
            "1D": 1440,
            "4H": 240,
            "1H": 60,
            "1W": 10080
        }

        try:
            interval = timeframe_mapping.get(timeframe, 60)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.get_lookback_days(timeframe))
            ohlc, last = self.api.get_ohlc_data(pair, interval=interval, since=start_date.timestamp())
            ohlc = ohlc.iloc[::-1]
            ohlc_cleaned = ohlc.fillna(0)
            ohlc_for_plot = ohlc_cleaned[['open', 'high', 'low', 'close', 'volume']]
            return ohlc_for_plot
        except Exception as e:
            st.error(f"Error al obtener datos para el par {pair}: {e}")
            return None

    def calculate_stochastic(self, ohlc_data, window=14):
<<<<<<< HEAD
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
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10, 8))
=======
        high_max = np.maximum.accumulate(ohlc_data['high'].values)
        low_min = np.minimum.accumulate(ohlc_data['low'].values)
        ohlc_data['%K'] = 100 * ((ohlc_data['close'].values - low_min) / (high_max - low_min))
        ohlc_data['%D'] = ohlc_data['%K'].rolling(window=window).mean()
        return ohlc_data

    def adjust_bar_width(self, selected_timeframe):
        if selected_timeframe == "1W":
            return 2.5
        elif selected_timeframe in ["4H"]:
            return 0.1
        elif selected_timeframe in ["1H"]:
            return 0.03  # Ajustado el ancho de las barras para 4H y 1H
        else:
            return 0.6

    def plot_candlestick_chart(self, ohlc_data, selected_pair, selected_timeframe):
        ohlc_data = self.calculate_stochastic(ohlc_data)
>>>>>>> developer

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3, 1, 1]}, sharex=True, figsize=(10, 8))

        if selected_timeframe in ["4H", "1H"]:
            ohlc_data = ohlc_data.iloc[-60:]  # Aumentado el número de velas para 4H y 1H

        mpf.plot(ohlc_data, type='candle', style='yahoo', ax=ax1, show_nontrading=True, ylabel='Precio (USDT)')

        ax1.yaxis.tick_left()
        ax1.xaxis.set_major_locator(plt.AutoLocator())
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: pd.to_datetime(x).strftime('%Y-%m-%d')))
        ax1.set_xlim(left=ohlc_data.index[0], right=ohlc_data.index[-1])

        width = self.adjust_bar_width(selected_timeframe)

        ax2.bar(ohlc_data.index, ohlc_data['volume'], color=np.where(ohlc_data['close'] > ohlc_data['open'], 'g', 'r'), width=width)
        ax2.set_ylabel('Volumen (USDT)')

        ax2.yaxis.tick_left()
        ax2.xaxis.set_major_locator(plt.AutoLocator())

        ax3.plot(ohlc_data.index, ohlc_data['%K'], label='Standard Stochastic', color='blue')
        ax3.plot(ohlc_data.index, ohlc_data['%D'], label='MA Stochastic', color='orange')
        ax3.axhline(80, color='red', linestyle='--', label='Overbought (80)')
        ax3.axhline(20, color='green', linestyle='--', label='Oversold (20)')

        ax3.set_xlabel('Fecha')
        ax3.set_ylabel('Estocástico')
        ax3.legend(loc='upper left')

        for line in ax1.lines + ax3.lines:
            line.set_picker(True)
            line.set_pickradius(5)
            line.set_label(line.get_label())

        def onpick(event):
            if event.artist in ax1.lines + ax3.lines:
                date = event.artist.get_xdata()[event.ind][0]
                label = ohlc_data.index[ohlc_data.index.get_loc(date)].strftime('%Y-%m-%d')
                st.write(f"Fecha: {label}, Precio de cierre: {ohlc_data.loc[label, 'close']:.2f}")

        fig.canvas.mpl_connect('pick_event', onpick)

        # Eliminar fechas del gráfico del estocástico
        ax3.set_xticks([])

<<<<<<< HEAD
        # Graficar estocástico
        ax2.plot(ohlc_data.index, ohlc_data['%K'], label='%K', color='blue')
        ax2.plot(ohlc_data.index, ohlc_data['%D'], label='%D', color='orange')
        ax2.axhline(80, color='red', linestyle='--', label='Overbought (80)')
        ax2.axhline(20, color='green', linestyle='--', label='Oversold (20)')

        # Ajustes de diseño
=======
>>>>>>> developer
        fig.suptitle(f'Gráfico {selected_pair} - Temporalidad {selected_timeframe}', fontsize=16)

<<<<<<< HEAD
        # Ajuste de escala en el eje y del segundo subgráfico
        ax2.set_ylim(0, 100)

        # Mostrar la gráfica en Streamlit
=======
>>>>>>> developer
        st.pyplot(fig)

def main():
    crypto_chart = CryptoChart()
    selected_pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "ATOMUSDT", "DOGEUSDT", "ROSEUSDT", "SOLUSDT", "MATICUSDT", "HBARUSDT"]
    selected_pair = st.selectbox('Selecciona un par de criptomonedas:', selected_pairs)
    selected_timeframes = ["1W", "1D", "4H", "1H"]
    selected_timeframe = st.selectbox('Selecciona la temporalidad:', selected_timeframes)
    ohlc_data = crypto_chart.get_ohlc_data(selected_pair, selected_timeframe)

    if ohlc_data is not None:
        crypto_chart.plot_candlestick_chart(ohlc_data, selected_pair, selected_timeframe)

if __name__ == "__main__":
    main()
