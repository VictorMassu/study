
# exchanges/binance.py
import os
import time
import requests
import hmac
import hashlib
from utils.logger import setup_logger
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

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

def verificar_saldo_binance(moeda):
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
        conta = client.get_asset_balance(asset=moeda)

        if conta and "free" in conta:
            saldo = float(conta["free"])
            logger.info(f"[Binance] Saldo disponível de {moeda}: {saldo}")
            return saldo
        else:
            logger.warning(f"[Binance] Saldo não encontrado para {moeda}")
            return 0.0
    except Exception as e:
        logger.error(f"[Binance] Erro ao verificar saldo: {e}")
        return 0.0