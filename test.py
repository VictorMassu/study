import time
import hashlib
import hmac
import requests
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL

def gerar_assinatura(secret, payload):
    return hmac.new(
        bytes(secret, "utf-8"),
        bytes(payload, "utf-8"),
        hashlib.sha256
    ).hexdigest()

def obter_saldo_bybit(coin="USDT"):
    try:
        endpoint = "/v5/account/wallet-balance"
        url = BYBIT_BASE_URL + endpoint

        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        query_string = f"accountType=UNIFIED&coin={coin}"
        payload = timestamp + BYBIT_API_KEY + recv_window + query_string

        signature = gerar_assinatura(BYBIT_API_SECRET, payload)

        headers = {
            "X-BAPI-API-KEY": BYBIT_API_KEY,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window
        }

        params = {
            "accountType": "UNIFIED",
            "coin": coin
        }

        response = requests.get(url, headers=headers, params=params)
        print("🛰️ Response status:", response.status_code)
        print("🧾 Raw response:", response.text)
        response.raise_for_status()

        data = response.json()
        if data.get("retCode") == 0:
            saldo = data["result"]["list"][0]["coin"][0]["walletBalance"]
            print(f"✅ Saldo de {coin} na Bybit Testnet: {saldo}")
        else:
            print(f"❌ Erro da API: {data}")

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    obter_saldo_bybit("USDT")
