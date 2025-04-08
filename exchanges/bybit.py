# exchanges/bybit.py

import time
import hmac
import hashlib
import requests
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL
from utils.logger import setup_logger
from exchanges.base import ExchangeBase

logger = setup_logger()

class BybitExchange(ExchangeBase):
    def __init__(self):
        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET
        self.base_url = BYBIT_BASE_URL

    def obter_preco(self, par):
        try:
            url = f"{self.base_url}/v5/market/tickers?category=linear&symbol={par}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data['retCode'] != 0:
                raise ValueError(data['retMsg'])

            resultado = data['result']['list'][0]
            preco_compra = float(resultado['bid1Price'])
            preco_venda = float(resultado['ask1Price'])
            logger.info(f"[Bybit] {par} - Compra: {preco_compra}, Venda: {preco_venda}")
            return preco_compra, preco_venda
        except Exception as e:
            logger.error(f"[Bybit] Erro ao obter preço para {par}: {e}")
            return None, None

    def verificar_saldo(self, moeda):
        try:
            timestamp = str(int(time.time() * 1000))
            payload = f"{timestamp}{self.api_key}5000"
            assinatura = hmac.new(
                self.api_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            headers = {
                "X-BAPI-API-KEY": self.api_key,
                "X-BAPI-SIGN": assinatura,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-RECV-WINDOW": "5000",
                "X-BAPI-SIGN-TYPE": "2"
            }

            url = f"{self.base_url}/v5/asset/transfer/query-asset-info?accountType=FUND"
            response = requests.get(url, headers=headers)
            data = response.json()
            for ativo in data.get("result", {}).get("balance", []):
                if ativo.get("coin") == moeda:
                    saldo = float(ativo.get("walletBalance", 0))
                    logger.info(f"[Bybit] Saldo disponível de {moeda}: {saldo}")
                    return saldo
            return 0.0
        except Exception as e:
            logger.error(f"[Bybit] Erro ao verificar saldo: {e}")
            return 0.0

    def enviar_ordem(self, par, side, quantidade, preco):
        """
        Envia uma ordem LIMIT para a Bybit via API v5.
        """
        try:
            timestamp = str(int(time.time() * 1000))
            body = {
                "category": "linear",
                "symbol": par,
                "side": side.upper(),
                "orderType": "Limit",
                "qty": str(quantidade),
                "price": str(preco),
                "timeInForce": "GTC"
            }
            body_str = json.dumps(body, separators=(',', ':'))
            payload = f"{timestamp}{self.api_key}5000{body_str}"

            assinatura = hmac.new(
                self.api_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            headers = {
                "X-BAPI-API-KEY": self.api_key,
                "X-BAPI-SIGN": assinatura,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-RECV-WINDOW": "5000",
                "X-BAPI-SIGN-TYPE": "2",
                "Content-Type": "application/json"
            }

            url = f"{self.base_url}/v5/order/create"

            logger.info(f"[Bybit] Enviando ordem {side} | {par} | Qtd: {quantidade} | Preço: {preco}")
            response = requests.post(url, headers=headers, data=body_str)
            resposta = response.json()

            if resposta.get("retCode") == 0:
                ordem_id = resposta['result'].get('orderId')
                logger.info(f"[Bybit] Ordem enviada com sucesso. ID: {ordem_id}")
                return resposta
            else:
                logger.error(f"[Bybit] Erro na resposta da ordem: {resposta}")
                return None
        except Exception as e:
            logger.error(f"[Bybit] Erro inesperado ao enviar ordem: {e}")
            return None
