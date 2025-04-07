import time
import hmac
import hashlib
import requests
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL

def gerar_assinatura(secret, query_string, timestamp, recv_window="5000"):
    return hmac.new(
        bytes(secret, "utf-8"),
        bytes(f"{timestamp}{BYBIT_API_KEY}{recv_window}{query_string}", "utf-8"),
        hashlib.sha256
    ).hexdigest()

def consultar_redes_deposito_bybit(moeda="USDC"):
    try:
        timestamp = str(int(time.time() * 1000))
        recv_window = "5000"
        endpoint = "/v5/asset/coin/query-info"
        params = f"coin={moeda}"
        signature = gerar_assinatura(BYBIT_API_SECRET, params, timestamp)

        headers = {
            "X-BAPI-API-KEY": BYBIT_API_KEY,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": recv_window,
            "X-BAPI-SIGN-TYPE": "2"
        }

        url = f"{BYBIT_BASE_URL}{endpoint}?{params}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 🔍 LOG BRUTO:
        print("\n📦 Resposta bruta da API:\n")
        import json
        print(json.dumps(data, indent=2))

        # 🎯 Mostra as redes disponíveis (se houver)
        chains = data.get("result", {}).get("chains", [])
        if chains:
            print(f"\n🔍 Redes disponíveis para depósito de {moeda} na Bybit:\n")
            for rede in chains:
                print(f"🔗 {rede.get('chainType')} - Status: {rede.get('chainDeposit')}")
        else:
            print("⚠️ Nenhuma rede de depósito encontrada para essa moeda.")

    except Exception as e:
        print(f"❌ Erro ao consultar redes de depósito: {e}")

if __name__ == "__main__":
    consultar_redes_deposito_bybit("USDC")  # ou troque por outra moeda, ex: "USDT"
