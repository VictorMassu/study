
# exchanges/bybit.py

import requests
from config import BYBIT_BASE_URL
from utils.logger import setup_logger

logger = setup_logger()

BYBIT_SYMBOL_MAP = {
    "BTCUSDT": "BTCUSDT",
    "ETHUSDT": "ETHUSDT"
}

def obter_preco_bybit(par):
    try:
        symbol = BYBIT_SYMBOL_MAP.get(par, par)
        url = f"{BYBIT_BASE_URL}/v5/market/tickers?category=spot&symbol={symbol}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['result'] and 'list' in data['result'] and data['result']['list']:
            ticker = data['result']['list'][0]
            preco_compra = float(ticker['bid1Price'])
            preco_venda = float(ticker['ask1Price'])
            logger.info(f"[Bybit] {par} - Compra: {preco_compra}, Venda: {preco_venda}")
            return preco_compra, preco_venda
        else:
            logger.warning(f"[Bybit] Nenhum dado retornado para {par}")
            return None, None
    except Exception as e:
        logger.error(f"Erro ao obter preço da Bybit para {par}: {e}")
        return None, None
