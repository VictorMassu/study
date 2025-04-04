
# executor_ordens_bybit.py
# Envia ordens LIMIT reais na Bybit Testnet

import time
import hmac
import hashlib
import requests
import json
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL, MODO_SIMULACAO
from utils.logger import setup_logger

logger = setup_logger()

def enviar_ordem_bybit(par, side, quantidade, preco):
    if MODO_SIMULACAO:
        logger.info(f"[SIMULAÇÃO] Ordem {side} na Bybit NÃO enviada (modo simulação).")
        return

    logger.info(f"[BYBIT] Enviando ordem {side} LIMIT para {par} | Quantidade: {quantidade}, Preço: {preco}")

    url = f"{BYBIT_BASE_URL}/v5/order/create"
    timestamp = str(int(time.time() * 1000))

    body = {
        "category": "spot",
        "symbol": par,
        "side": side,
        "orderType": "Limit",
        "qty": quantidade,
        "price": preco,
        "timeInForce": "GTC"
    }

    recv_window = "5000"
    param_str = f"{timestamp}{BYBIT_API_KEY}{recv_window}{json.dumps(body, separators=(',', ':'))}"
    signature = hmac.new(BYBIT_API_SECRET.encode("utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "X-BAPI-SIGN": signature,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        data = response.json()
        logger.info(f"[BYBIT] Ordem enviada com sucesso: {data}")
        return data
    except Exception as e:
        logger.error(f"[BYBIT] Erro ao enviar ordem: {e}")
        return None
