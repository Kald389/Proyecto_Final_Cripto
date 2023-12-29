import pytest
import plotly.graph_objects as go
import pandas as pd
from main import DataFetcher, IndicatorCalculator, ChartPlotter

@pytest.fixture
def data_fetcher():
    return DataFetcher()

def test_get_lookback_days():
    data_fetcher = DataFetcher()
    assert data_fetcher.get_lookback_days("1D") == 90

@pytest.fixture
def indicator_calculator():
    return IndicatorCalculator()

def test_calculate_stochastic(indicator_calculator):
    ohlc_data = pd.DataFrame({
        'open': [1, 2, 3],
        'high': [4, 5, 6],
        'low': [1, 2, 3],
        'close': [4, 5, 6],
        'volume': [100, 200, 300]
    })
    result = indicator_calculator.calculate_stochastic(ohlc_data)
    assert 'close' in result.columns
    assert '%K' in result.columns
    assert '%D' in result.columns

@pytest.fixture
def chart_plotter():
    return ChartPlotter()

def test_adjust_bar_width(chart_plotter):
    assert chart_plotter.adjust_bar_width("1W") == 2.5

# Para DataFetcher
def test_get_ohlc_data(data_fetcher):
    pair = "BTCUSDT"
    timeframe = "1D"
    ohlc_data = data_fetcher.get_ohlc_data(pair, timeframe)
    assert ohlc_data is not None
    assert isinstance(ohlc_data, pd.DataFrame)
    assert 'open' in ohlc_data.columns
    assert 'high' in ohlc_data.columns
    assert 'low' in ohlc_data.columns
    assert 'close' in ohlc_data.columns
    assert 'volume' in ohlc_data.columns

# Para IndicatorCalculator
def test_calculate_stochastic_with_custom_window(indicator_calculator):
    ohlc_data = pd.DataFrame({
        'open': [1, 2, 3],
        'high': [4, 5, 6],
        'low': [1, 2, 3],
        'close': [4, 5, 6],
        'volume': [100, 200, 300]
    })
    window = 10
    result = indicator_calculator.calculate_stochastic(ohlc_data, window=window)
    assert 'close' in result.columns
    assert '%K' in result.columns
    assert '%D' in result.columns

# Para ChartPlotter
def test_plot_candlestick_chart(chart_plotter):
    ohlc_data = pd.DataFrame({
        'open': [1, 2, 3],
        'high': [4, 5, 6],
        'low': [1, 2, 3],
        'close': [4, 5, 6],
        'volume': [100, 200, 300]
    })
    selected_pair = "BTCUSDT"
    selected_timeframe = "1D"
    fig = chart_plotter.plot_candlestick_chart(ohlc_data, selected_pair, selected_timeframe)
    assert fig is not None
    assert isinstance(fig, go.Figure)
    # Añade más aserciones según las características que quieras comprobar en el gráfico.

# Para DataFetcher
def test_get_ohlc_data_with_invalid_pair(data_fetcher):
    pair = "INVALID_PAIR"
    timeframe = "1D"
    ohlc_data = data_fetcher.get_ohlc_data(pair, timeframe)
    assert ohlc_data is None

# Para IndicatorCalculator
def test_calculate_stochastic_with_empty_data(indicator_calculator):
    ohlc_data = pd.DataFrame()
    result = indicator_calculator.calculate_stochastic(ohlc_data)
    assert result.empty

# Para ChartPlotter
def test_plot_candlestick_chart_with_invalid_data(chart_plotter):
    ohlc_data = pd.DataFrame()  # Datos vacíos
    selected_pair = "BTCUSDT"
    selected_timeframe = "1D"
    fig = chart_plotter.plot_candlestick_chart(ohlc_data, selected_pair, selected_timeframe)
    assert fig is None

def test_plot_candlestick_chart_with_invalid_timeframe(chart_plotter):
    ohlc_data = pd.DataFrame({
        'open': [1, 2, 3],
        'high': [4, 5, 6],
        'low': [1, 2, 3],
        'close': [4, 5, 6],
        'volume': [100, 200, 300]
    })
    selected_pair = "BTCUSDT"
    selected_timeframe = "INVALID_TIMEFRAME"
    fig = chart_plotter.plot_candlestick_chart(ohlc_data, selected_pair, selected_timeframe)
    assert fig is None


