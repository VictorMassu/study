# exchanges/binance.py

import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException
from utils.logger import setup_logger
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL  # Usando a URL dinâmica
from exchanges.base import ExchangeBase

logger = setup_logger()

class BinanceExchange(ExchangeBase):
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        self.client.API_URL = BINANCE_BASE_URL  # Usando a URL dinâmica

    def obter_preco(self, par):
        try:
            url = f"{BINANCE_BASE_URL}/api/v3/ticker/bookTicker?symbol={par}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            preco_compra = float(data['bidPrice'])
            preco_venda = float(data['askPrice'])
            logger.info(f"[Binance] {par} - Compra: {preco_compra}, Venda: {preco_venda}")
            return preco_compra, preco_venda
        except Exception as e:
            logger.error(f"[Binance] Erro ao obter preço para {par}: {e}")
            return None, None
        
    def verificar_saldo(self, moeda):
        try:
            info = self.client.get_asset_balance(asset=moeda)
            saldo = float(info['free']) if info else 0.0
            logger.info(f"[Binance] Saldo de {moeda}: {saldo}")
            return saldo
        except Exception as e:
            logger.error(f"[Binance] Erro ao verificar saldo de {moeda}: {e}")
            return 0.0


    def enviar_ordem(self, par, side, quantidade, preco):
        try:
            ordem = self.client.create_order(
                symbol=par,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=quantidade,
                price=preco
            )
            logger.info(f"[Binance] Ordem enviada: {ordem}")
            return ordem
        except BinanceAPIException as e:
            logger.error(f"[Binance] Erro na API: {e.message}")
            return None
        except Exception as e:
            logger.error(f"[Binance] Erro inesperado ao enviar ordem: {e}")
            return None
