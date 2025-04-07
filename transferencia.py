# transferencia.py
import time
import requests
import hmac
import hashlib
from config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_BASE_URL
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL
from utils.logger import setup_logger

logger = setup_logger()

def gerar_assinatura_binance(secret, query_string):
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def gerar_assinatura_bybit(secret, params, timestamp, api_key, recv_window):
    sorted_params = sorted(params.items())
    query_string = '&'.join(f"{k}={v}" for k, v in sorted_params)
    origin_string = f"{timestamp}{api_key}{recv_window}{query_string}"
    return hmac.new(secret.encode("utf-8"), origin_string.encode("utf-8"), hashlib.sha256).hexdigest()

def get_endereco_deposito_binance(moeda="USDT", rede="POLYGON"):
    try:
        endpoint = "/sapi/v1/capital/deposit/address"
        timestamp = str(int(time.time() * 1000))
        params = f"coin={moeda}&network={rede}&timestamp={timestamp}"
        signature = gerar_assinatura_binance(BINANCE_API_SECRET, params)

        headers = {
            "X-MBX-APIKEY": BINANCE_API_KEY
        }

        url = f"{BINANCE_BASE_URL}{endpoint}?{params}&signature={signature}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        endereco = data.get("address")
        logger.info(f"[BINANCE] Endereço de depósito {moeda} ({rede}): {endereco}")
        return endereco
    except Exception as e:
        logger.error(f"[BINANCE] Erro ao obter endereço de depósito: {e}")
        return None

def get_endereco_deposito_bybit(moeda="USDT", rede="Polygon"):
    try:
        endpoint = "/v5/asset/deposit/address"
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        params = {
            "coin": moeda,
            "chainType": rede,
            "timestamp": timestamp,
            "recvWindow": recv_window
        }

        assinatura = gerar_assinatura_bybit(BYBIT_API_SECRET, params, timestamp, BYBIT_API_KEY, recv_window)

        headers = {
            "X-BAPI-API-KEY": BYBIT_API_KEY,
            "X-BAPI-SIGN": assinatura,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "X-BAPI-SIGN-TYPE": "2"
        }

        response = requests.get(f"{BYBIT_BASE_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        endereco = data["result"]["address"]
        logger.info(f"[BYBIT] Endereço de depósito {moeda} ({rede}): {endereco}")
        return endereco
    except Exception as e:
        logger.error(f"[BYBIT] Erro ao obter endereço de depósito: {e}")
        return None

# Em seguida, criaremos a função para solicitar saque em ambas as exchanges.
# Vamos adicionar essa função no próximo passo, com a simulação opcional.

if __name__ == "__main__":
    logger.info("Consultando endereços de depósito...")
    endereco_bybit = get_endereco_deposito_bybit()
    endereco_binance = get_endereco_deposito_binance()
