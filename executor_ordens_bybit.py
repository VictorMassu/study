# executor_ordens_bybit.py
import time
import hmac
import hashlib
import requests
import json
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL
from utils.logger import setup_logger

logger = setup_logger()

def enviar_ordem_bybit(par, side, quantidade, preco):
    try:
        timestamp = str(int(time.time() * 1000))
        endpoint = "/v5/order/create"
        url = BYBIT_BASE_URL + endpoint

        body = {
            "category": "spot",
            "symbol": par,
            "side": side,
            "orderType": "Limit",
            "qty": quantidade,
            "price": preco,
            "timeInForce": "GTC"
        }

        headers = {
            "Content-Type": "application/json",
            "X-BAPI-API-KEY": BYBIT_API_KEY,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": "5000",
        }

        # assinatura específica da API v5
        sign_payload = timestamp + BYBIT_API_KEY + "5000" + json.dumps(body)
        signature = hmac.new(bytes(BYBIT_API_SECRET, "utf-8"), sign_payload.encode("utf-8"), hashlib.sha256).hexdigest()
        headers["X-BAPI-SIGN"] = signature

        logger.info(f"[BYBIT] Enviando ordem {side} LIMIT para {par} | Quantidade: {quantidade}, Preço: {preco}")
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        if response.json().get("retCode") == 170131:
            logger.warning("[BYBIT] Saldo insuficiente para realizar a ordem.")
        logger.info(f"[BYBIT] Ordem enviada com sucesso: {response.json()}")
    except Exception as e:
        logger.error(f"[BYBIT] Erro ao enviar ordem: {e}")
