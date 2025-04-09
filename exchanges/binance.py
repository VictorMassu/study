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

    def obter_pares_validos(self):
        """
        Consulta os pares válidos na Binance para verificar se o par está disponível.
        """
        try:
            url = f"{BINANCE_BASE_URL}/api/v3/exchangeInfo"  # Endpoint correto da Binance
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            pares_validos = {symbol['symbol'] for symbol in data['symbols'] if symbol['status'] == 'TRADING'}
            logger.info(f"Parâmetros válidos na Binance: {pares_validos}")
            return pares_validos
        except Exception as e:
            logger.error(f"[Binance] Erro ao obter pares válidos: {e}")
            return set()

    def obter_preco(self, par):
        """
        Obtém o preço de compra e venda para um par válido na Binance.
        """
        pares_validos = self.obter_pares_validos()

        if par not in pares_validos:
            logger.warning(f"Par {par} não é válido na Binance. Pulando análise.")
            return None, None

        try:
            url = f"{BINANCE_BASE_URL}/v3/ticker/bookTicker?symbol={par}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            preco_compra = float(data['bidPrice'])
            preco_venda = float(data['askPrice'])
            logger.info(f"[Binance] {par} - Compra: {preco_compra}, Venda: {preco_venda}")
            return preco_compra, preco_venda
        except BinanceAPIException as e:
            logger.error(f"[Binance] Erro na API: {e.message}")
            return None, None
        except Exception as e:
            logger.error(f"[Binance] Erro inesperado ao obter preço: {e}")
            return None, None


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
