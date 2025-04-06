import os
import time
import requests
import hmac
import hashlib
from utils.logger import setup_logger
from config import BYBIT_BASE_URL
import logging
from collections import OrderedDict

logger = setup_logger()

BYBIT_SYMBOL_MAP = {
    "BTCUSDT": "BTCUSDT",
    "ETHUSDT": "ETHUSDT"
}

# Obtém preços atuais da Bybit para o par especificado
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

def gerar_assinatura(secret, params, timestamp, api_key, recv_window):
    """
    Monta a string a ser assinada conforme especificado na documentação oficial da Bybit API v5.
    """
    sorted_params = sorted(params.items())
    query_string = '&'.join(f"{k}={v}" for k, v in sorted_params)
    origin_string = f"{timestamp}{api_key}{recv_window}{query_string}"
    return hmac.new(secret.encode("utf-8"), origin_string.encode("utf-8"), hashlib.sha256).hexdigest()

def verificar_saldo_bybit(api_key, api_secret, simbolo="USDT"):
    """
    Verifica o saldo disponível para um determinado ativo na conta UNIFICADA da Bybit Testnet.
    Retorna o saldo disponível ou None em caso de erro.
    """
    try:
        endpoint = "/v5/account/wallet-balance"
        url = BYBIT_BASE_URL + endpoint
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"

        params = {
            "accountType": "UNIFIED",
            "coin": simbolo,
        }

        sign = gerar_assinatura(api_secret, params, timestamp, api_key, recv_window)

        headers = {
            "X-BAPI-API-KEY": api_key,
            "X-BAPI-SIGN": sign,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "X-BAPI-SIGN-TYPE": "2"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("retCode") == 0:
            saldo = float(data["result"]["list"][0]["coin"][0]["walletBalance"])
            logger.info(f"[Bybit] Saldo disponível de {simbolo}: {saldo}")
            return saldo
        else:
            logger.error(f"[Bybit] Erro da API: {data}")
            return None

    except Exception as e:
        logger.error(f"[Bybit] Erro inesperado: {e}")
        return None