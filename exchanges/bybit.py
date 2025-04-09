# exchanges/bybit.py

import time
import hmac
import hashlib
import requests
import json
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL
from utils.logger import setup_logger
from exchanges.base import ExchangeBase

logger = setup_logger()


def safe_request(method, url, headers=None, params=None, data=None):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data, timeout=10)
        else:
            raise ValueError("Método HTTP não suportado")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"[Bybit] Erro na requisição HTTP: {e}")
        return None
    except Exception as e:
        logger.error(f"[Bybit] Erro inesperado: {e}")
        return None


class BybitExchange(ExchangeBase):
    def __init__(self):
        self.api_key = BYBIT_API_KEY
        self.api_secret = BYBIT_API_SECRET
        self.base_url = BYBIT_BASE_URL

    def obter_preco(self, par):
        url = f"{self.base_url}/v5/market/tickers"
        params = {"category": "spot", "symbol": par}
        data = safe_request("GET", url, params=params)

        if not data or data.get('retCode') != 0:
            logger.warning(f"[Bybit] Erro ao obter preço para {par}: {data.get('retMsg', 'Erro desconhecido')}")
            return None, None

        resultado = data['result']['list'][0]
        bid_price = resultado.get('bid1Price', '')
        ask_price = resultado.get('ask1Price', '')

        if not bid_price or not ask_price:
            logger.warning(f"[Bybit] Preços vazios para {par}, ignorando...")
            return None, None

        try:
            preco_compra = float(bid_price)
            preco_venda = float(ask_price)
            logger.info(f"[Bybit] {par} - Compra: {preco_compra}, Venda: {preco_venda}")
            return preco_compra, preco_venda
        except Exception as e:
            logger.error(f"[Bybit] Erro ao converter preços para {par}: {e}")
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

            url = f"{self.base_url}/v5/account/wallet-balance"
            params = {"accountType": "UNIFIED"}
            data = safe_request("GET", url, headers=headers, params=params)

            if data and data.get("retCode") == 0:
                saldo = next((float(m["availableBalance"]) for m in data["result"]["list"] if m["coin"] == moeda), 0.0)
                logger.info(f"[Bybit] Saldo de {moeda}: {saldo}")
                return saldo
            else:
                logger.error(f"[Bybit] Erro ao verificar saldo: {data}")
                return 0.0
        except Exception as e:
            logger.error(f"[Bybit] Erro inesperado ao verificar saldo de {moeda}: {e}")
            return 0.0

    def enviar_ordem(self, par, side, quantidade, preco):
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
            resposta = safe_request("POST", url, headers=headers, data=body_str)

            if resposta and resposta.get("retCode") == 0:
                ordem_id = resposta['result'].get('orderId')
                logger.info(f"[Bybit] Ordem enviada com sucesso. ID: {ordem_id}")
                return resposta
            else:
                logger.error(f"[Bybit] Erro na resposta da ordem: {resposta}")
                return None
        except Exception as e:
            logger.error(f"[Bybit] Erro inesperado ao enviar ordem: {e}")
            return None
