import streamlit as st
import matplotlib.pyplot as plt
import mplfinance as mpf
from pykrakenapi import KrakenAPI
import krakenex

# Función para obtener datos OHLC de Kraken
def get_ohlc_data(pair, interval=60):
    try:
        ohlc, last = api.get_ohlc_data(pair, interval=interval)
        ohlc = ohlc.iloc[::-1]
        ohlc_cleaned = ohlc.fillna(0)
        ohlc_for_plot = ohlc_cleaned[['open', 'high', 'low', 'close', 'volume']]
        return ohlc_for_plot
    except Exception as e:
        st.error(f"Error al obtener datos para el par {pair}: {e}")
        return None

# Crear una instancia de la clase krakenex.API
api_krakenex = krakenex.API()
# Pasar la instancia de krakenex.API a KrakenAPI
api = KrakenAPI(api_krakenex)

# Lista de pares específicos
selected_pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "ATOMUSDT", "DOGEUSDT", "ROSEUSDT", "SOLUSDT", "MATICUSDT", "HBARUSDT"]

# Seleccionar par mediante un widget de Streamlit
selected_pair = st.selectbox('Selecciona un par de criptomonedas:', selected_pairs)

# Obtener datos OHLC para el par seleccionado
ohlc_data = get_ohlc_data(selected_pair)

if ohlc_data is not None:
    # Crear una figura
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True, figsize=(10, 8))

    # Graficar velas japonesas en el primer eje
    mpf.plot(ohlc_data, type='candle', style='yahoo', ax=ax1, show_nontrading=True)

    # Agregar volumen al segundo eje
    ax2.fill_between(ohlc_data.index, ohlc_data['volume'], color='gray', alpha=0.5)
    ax2.set_xlabel('Fecha')
    ax2.set_ylabel('Volumen')

    # Ajustes de diseño
    fig.suptitle(f'Gráfico {selected_pair}', fontsize=16)
    plt.tight_layout()

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)
