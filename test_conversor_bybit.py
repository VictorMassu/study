import time
import hmac
import hashlib
import requests
import json
from config import BYBIT_API_KEY, BYBIT_API_SECRET, BYBIT_BASE_URL

def gerar_assinatura(secret, body_str, timestamp):
    """
    Gera a assinatura exigida pela Bybit v5 para requisições POST com JSON.
    """
    message = f"{timestamp}{BYBIT_API_KEY}5000{body_str}"
    return hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()

def consultar_saldos_bybit():
    print("\n🔍 Consultando saldos disponíveis na Bybit Testnet...\n")
    endpoint = "/v5/account/wallet-balance"
    url = BYBIT_BASE_URL + endpoint
    timestamp = str(int(time.time() * 1000))
    params = {
        "accountType": "UNIFIED"
    }

    query_string = '&'.join(f"{k}={v}" for k, v in sorted(params.items()))
    signature = hmac.new(
        BYBIT_API_SECRET.encode("utf-8"),
        f"{timestamp}{BYBIT_API_KEY}5000{query_string}".encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": "5000",
        "X-BAPI-SIGN-TYPE": "2"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if data["retCode"] == 0:
        moedas = data["result"]["list"][0]["coin"]
        for coin in moedas:
            livre = float(coin["walletBalance"])
            if livre > 0:
                print(f"🪙 {coin['coin']}: Livre = {livre}, Travado = {coin['locked']}")
    else:
        print("❌ Erro ao consultar saldos:", data)

def converter_moeda_bybit():
    consultar_saldos_bybit()

    print("\n🧾 Vamos realizar uma conversão de saldo.\n")
    moeda_origem = input("Digite a moeda que você quer VENDER (ex: BTC): ").upper()
    moeda_destino = input("Digite a moeda que você quer RECEBER (ex: USDT): ").upper()
    quantidade = input(f"Digite a quantidade de {moeda_origem} para converter: ").strip()

    try:
        quantidade_float = float(quantidade)
    except ValueError:
        print("❌ Quantidade inválida.")
        return

    endpoint = "/v5/asset/exchange/convert"
    url = BYBIT_BASE_URL + endpoint
    timestamp = str(int(time.time() * 1000))

    body = {
        "fromCoin": moeda_origem,
        "toCoin": moeda_destino,
        "fromAmount": quantidade,
        "marketUnit": "fromCoin"
    }
    body_str = json.dumps(body)

    signature = gerar_assinatura(BYBIT_API_SECRET, body_str, timestamp)

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": "5000",
        "X-BAPI-SIGN-TYPE": "2",
        "Content-Type": "application/json"
    }

    confirmar = input(f"\n⚠️ Deseja realmente converter {quantidade} {moeda_origem} para {moeda_destino}? (s/n): ").strip().lower()
    if confirmar != "s":
        print("❌ Operação cancelada.")
        return

    response = requests.post(url, headers=headers, data=body_str)
    data = response.json()

    if data.get("retCode") == 0:
        print("✅ Conversão realizada com sucesso!")
        print(json.dumps(data["result"], indent=2))
    else:
        print("❌ Erro ao converter saldo:", data)

if __name__ == "__main__":
    try:
        converter_moeda_bybit()
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
