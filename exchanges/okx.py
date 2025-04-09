# exchanges/okx.py

import time
import hmac
import hashlib
import requests
import json
from config import OKX_API_KEY, OKX_API_SECRET, OKX_PASSPHRASE, OKX_BASE_URL, AMBIENTE
from utils.logger import setup_logger
from exchanges.base import ExchangeBase
import base64

logger = setup_logger()

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
        logger.error(f"[OKX] Erro na requisição HTTP: {e}")
        return None
    except Exception as e:
        logger.error(f"[OKX] Erro inesperado: {e}")
        return None


class OKXExchange(ExchangeBase):
    def __init__(self):
        self.api_key = OKX_API_KEY
        self.api_secret = OKX_API_SECRET
        self.passphrase = OKX_PASSPHRASE
        self.base_url = OKX_BASE_URL
        self.simulated = AMBIENTE == "test"

    def _auth_headers(self, method, endpoint, body=""):
        timestamp = str(time.time())
        prehash = f"{timestamp}{method}{endpoint}{body}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            prehash.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.b64encode(signature).decode()

        headers = {
            "Content-Type": "application/json",
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature_b64,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase
        }

        if self.simulated:
            headers["x-simulated-trading"] = "1"

        return headers

    def formatar_par(self, par):
        return par.replace("/", "-").upper()  # Ex: usdc/btc → USDC-BTC

    def obter_preco(self, par):
        symbol = self.formatar_par(par)
        endpoint = f"/api/v5/market/ticker?instId={symbol}"
        url = self.base_url + endpoint
        headers = self._auth_headers("GET", endpoint)

        data = safe_request("GET", url, headers=headers)

        if not data or "data" not in data or len(data["data"]) == 0:
            logger.warning(f"[OKX] Erro ao obter preço para {symbol}")
            return None, None

        try:
            preco_compra = float(data["data"][0]["bidPx"])
            preco_venda = float(data["data"][0]["askPx"])
            logger.info(f"[OKX] {symbol} - Compra: {preco_compra}, Venda: {preco_venda}")
            return preco_compra, preco_venda
        except Exception as e:
            logger.error(f"[OKX] Erro ao processar preço para {symbol}: {e}")
            return None, None

    def verificar_saldo(self, moeda):
        endpoint = "/api/v5/account/balance"
        url = self.base_url + endpoint
        headers = self._auth_headers("GET", endpoint)

        data = safe_request("GET", url, headers=headers)

        if data and "data" in data:
            for item in data["data"][0]["details"]:
                if item["ccy"] == moeda.upper():
                    saldo = float(item["availBal"])
                    logger.info(f"[OKX] Saldo de {moeda}: {saldo}")
                    return saldo

        logger.warning(f"[OKX] Não foi possível obter saldo de {moeda}")
        return 0.0

    def enviar_ordem(self, par, side, quantidade, preco):
        endpoint = "/api/v5/trade/order"
        url = self.base_url + endpoint
        symbol = self.formatar_par(par)
        body = {
            "instId": symbol,
            "tdMode": "cash",
            "side": side.lower(),
            "ordType": "limit",
            "px": str(preco),
            "sz": str(quantidade)
        }
        body_str = json.dumps(body)
        headers = self._auth_headers("POST", endpoint, body_str)

        logger.info(f"[OKX] Enviando ordem {side} | {symbol} | Qtd: {quantidade} | Preço: {preco}")
        resposta = safe_request("POST", url, headers=headers, data=body_str)

        if resposta and resposta.get("code") == "0":
            ordem_id = resposta["data"][0].get("ordId")
            logger.info(f"[OKX] Ordem enviada com sucesso. ID: {ordem_id}")
            return resposta
        else:
            logger.error(f"[OKX] Erro ao enviar ordem: {resposta}")
            return None