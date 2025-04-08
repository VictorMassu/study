# exchanges/registry.py

from exchanges.binance import BinanceExchange
from exchanges.bybit import BybitExchange

# Registro dinâmico de exchanges disponíveis no sistema
EXCHANGES = {
    "binance": BinanceExchange(),
    "bybit": BybitExchange()
}
