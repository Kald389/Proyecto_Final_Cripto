import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pykrakenapi import KrakenAPI
import krakenex
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
            return 30
        elif selected_timeframe == "1H":
            return 10
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
            return 0.03
        else:
            return 0.6

    def plot_candlestick_chart(self, ohlc_data, selected_pair, selected_timeframe):
        ohlc_data = self.calculate_stochastic(ohlc_data)

        # Gráfico de precio
        candlestick = go.Candlestick(x=ohlc_data.index,
                                     open=ohlc_data['open'],
                                     high=ohlc_data['high'],
                                     low=ohlc_data['low'],
                                     close=ohlc_data['close'],
                                     name='Candlestick')

        # Gráfico de volumen
        volume = go.Bar(x=ohlc_data.index, y=ohlc_data['volume'],
                        marker_color=np.where(ohlc_data['close'] > ohlc_data['open'], 'green', 'red'),
                        name='Volume')

        # Gráfico de estocástico
        stochastics = go.Scatter(x=ohlc_data.index, y=ohlc_data['%K'], mode='lines', name='%K', line=dict(color='blue'))
        stochastics_d = go.Scatter(x=ohlc_data.index, y=ohlc_data['%D'], mode='lines', name='%D', line=dict(color='orange'))

        # Configuración del gráfico principal (precio)
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=['Precio (USDT)', 'Volumen (USDT)', 'Estocástico'])
        fig.add_trace(candlestick, row=1, col=1)
        fig.add_trace(volume, row=2, col=1)
        fig.add_trace(stochastics, row=3, col=1)
        fig.add_trace(stochastics_d, row=3, col=1)

        width = self.adjust_bar_width(selected_timeframe)

        # Configuración del eje y
        fig.update_yaxes(title_text='Precio (USDT)', row=1, col=1)
        fig.update_yaxes(title_text='Volumen (USDT)', row=2, col=1)
        fig.update_yaxes(title_text='Estocástico', row=3, col=1)

        # Configuración del eje x
        fig.update_xaxes(type='category', categoryorder='category ascending', row=3, col=1)

        # Ajuste de diseño
        fig.update_layout(showlegend=False, height=800, title_text=f'Gráfico {selected_pair} - Temporalidad {selected_timeframe}', xaxis_rangeslider_visible=False)

        return fig

def main():
    crypto_chart = CryptoChart()
    selected_pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "ATOMUSDT", "DOGEUSDT", "ROSEUSDT", "SOLUSDT", "MATICUSDT", "HBARUSDT"]
    selected_pair = st.selectbox('Selecciona un par de criptomonedas:', selected_pairs)
    selected_timeframes = ["1W", "1D", "4H", "1H"]
    selected_timeframe = st.selectbox('Selecciona la temporalidad:', selected_timeframes)
    ohlc_data = crypto_chart.get_ohlc_data(selected_pair, selected_timeframe)

    if ohlc_data is not None:
        fig = crypto_chart.plot_candlestick_chart(ohlc_data, selected_pair, selected_timeframe)

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
