
# exchanges/bybit.py

import os
import time
import requests
import hmac
import hashlib
from utils.logger import setup_logger
from config import BYBIT_BASE_URL
from collections import OrderedDict


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
    
def gerar_assinatura(query_string):
    return hmac.new(
        os.getenv("BYBIT_API_SECRET").encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

from collections import OrderedDict
import urllib.parse

def verificar_saldo_bybit(par, side, quantidade_necessaria):
    try:
        from config import BYBIT_API_KEY, BYBIT_API_SECRET
        symbol_base = par.replace("USDT", "")
        moeda = "USDT" if side == "BUY" else symbol_base.upper()

        params = {
            "accountType": "UNIFIED",
            "recvWindow": "5000",
            "timestamp": str(int(time.time() * 1000))
        }

        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            BYBIT_API_SECRET.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        headers = {
            "X-BYBIT-API-KEY": BYBIT_API_KEY,
            "X-BYBIT-SIGN": signature,
            "X-BYBIT-TIMESTAMP": params["timestamp"],
            "X-BYBIT-RECV-WINDOW": params["recvWindow"],
        }

        url = f"{BYBIT_BASE_URL}/v5/account/wallet-balance?{query_string}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        for item in data['result']['list'][0]['coin']:
            if item['coin'] == moeda:
                saldo = float(item['availableToWithdraw'])
                logger.info(f"[Bybit] Saldo disponível de {moeda}: {saldo}")
                return saldo >= quantidade_necessaria

        logger.warning(f"[Bybit] Moeda {moeda} não encontrada no saldo.")
        return False

    except Exception as e:
        logger.error(f"[Bybit] Erro ao verificar saldo: {e}")
        return False
