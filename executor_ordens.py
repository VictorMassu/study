
# executor_ordens.py

import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from config import MODO_SIMULACAO, BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL
from utils.logger import setup_logger

logger = setup_logger()

def enviar_ordem_binance(par, side, quantidade, preco):
    if MODO_SIMULACAO:
        logger.info(f"[SIMULAÇÃO] Ordem {side} na Binance NÃO enviada (modo simulação).")
        return

    logger.info(f"[BINANCE] Enviando ordem {side} LIMIT para {par} | Quantidade: {quantidade}, Preço: {preco}")
    endpoint = "/v3/order"
    url = BINANCE_BASE_URL + endpoint
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": par,
        "side": side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": quantidade,
        "price": preco,
        "timestamp": timestamp
    }

    query_string = urlencode(params)
    signature = hmac.new(BINANCE_API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature
    headers = { "X-MBX-APIKEY": BINANCE_API_KEY }

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"[BINANCE] Ordem enviada com sucesso: {data}")
        return data
    except Exception as e:
        logger.error(f"[BINANCE] Erro ao enviar ordem: {e}")
        return None
