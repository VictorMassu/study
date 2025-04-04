
# exchanges/binance.py

import requests
from config import BINANCE_BASE_URL, BINANCE_API_KEY
from utils.logger import setup_logger

logger = setup_logger()

def obter_preco_binance(par):
    try:
        url = f"{BINANCE_BASE_URL}/v3/ticker/bookTicker?symbol={par}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        preco_compra = float(data['bidPrice'])
        preco_venda = float(data['askPrice'])
        logger.info(f"[Binance] {par} - Compra: {preco_compra}, Venda: {preco_venda}")
        return preco_compra, preco_venda
    except Exception as e:
        logger.error(f"Erro ao obter preço da Binance para {par}: {e}")
        return None, None
