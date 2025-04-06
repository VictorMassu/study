
# exchanges/bybit.py

import os
import time
import requests
import hmac
import hashlib
from utils.logger import setup_logger
from config import BYBIT_BASE_URL
from collections import OrderedDict
import logging


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

def verificar_saldo_bybit(api_key, api_secret, simbolo):
    try:
        # Endpoint da API para obter o saldo da carteira
        url = "https://api-testnet.bybit.com/v5/account/wallet-balance"
        
        # Parâmetros da requisição
        recv_window = 5000
        timestamp = int(time.time() * 1000)
        params = f"accountType=UNIFIED&coin={simbolo}&recvWindow={recv_window}&timestamp={timestamp}"
        
        # Assinatura HMAC para autenticação
        signature = hmac.new(
            bytes(api_secret, "utf-8"),
            bytes(params, "utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            "X-BYBIT-API-KEY": api_key,
            "X-BYBIT-SIGN": signature,
            "X-BYBIT-RECV-WINDOW": str(recv_window),
            "X-BYBIT-TIMESTAMP": str(timestamp)
        }
        
        # Faz a requisição GET
        response = requests.get(f"{url}?{params}", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Verifica se a resposta contém o saldo do ativo
        if data["retCode"] == 0:
            for balance in data["result"]["list"]:
                if balance["coin"] == simbolo:
                    return float(balance["free"])
            logging.warning(f"[Bybit] Ativo {simbolo} não encontrado na conta.")
            return 0.0
        else:
            logging.error(f"[Bybit] Erro na API: {data['retCode']} - {data['retMsg']}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"[Bybit] Erro na requisição: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"[Bybit] Erro inesperado: {str(e)}")
        return None
