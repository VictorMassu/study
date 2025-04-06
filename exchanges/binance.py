
# exchanges/binance.py
import os
import time
import requests
import hmac
import hashlib
from utils.logger import setup_logger
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL



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

def verificar_saldo_binance(par, side, quantidade_necessaria):
    try:
        moeda = "USDT" if side == "BUY" else par.replace("USDT", "")

        timestamp = int(time.time() * 1000)
        query_string = f"timestamp={timestamp}"
        signature = hmac.new(
            BINANCE_API_SECRET.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        url = f"{BINANCE_BASE_URL}/v3/ticker/bookTicker?symbol={par}"
        headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.warning(f"[Binance] Resposta da conta: {data}")
        if 'balances' not in data:
            logger.error("[Binance] Resposta inesperada da API (sem 'balances')")
            return False
        for asset in data['balances']:
            if asset['asset'] == moeda:
                saldo = float(asset['free'])
                logger.info(f"[Binance] Saldo disponível de {moeda}: {saldo}")
                return saldo >= quantidade_necessaria

        logger.warning(f"[Binance] Moeda {moeda} não encontrada no saldo.")
        return False
    except Exception as e:
        logger.error(f"[Binance] Erro ao verificar saldo: {e}")
        return False