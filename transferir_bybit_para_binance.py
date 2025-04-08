import time
import uuid
import hmac
import hashlib
import requests
import json
import logging
from config import BYBIT_API_KEY, BYBIT_API_SECRET

# Configuração do log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BYBIT_BASE_URL = "https://api.bybit.com"

def gerar_assinatura(secret, payload):
    return hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def consultar_saldo(moeda="USDC", conta="FUND"):
    timestamp = str(int(time.time() * 1000))
    endpoint = "/v5/asset/transfer/query-account-coins-balance"
    query_string = f"accountType={conta}&coin={moeda}"
    payload = f"{timestamp}{BYBIT_API_KEY}5000{query_string}"
    assinatura = gerar_assinatura(BYBIT_API_SECRET, payload)

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-SIGN": assinatura,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": "5000",
        "X-BAPI-SIGN-TYPE": "2"
    }

    url = f"{BYBIT_BASE_URL}{endpoint}?{query_string}"
    try:
        response = requests.get(url, headers=headers)
        logging.debug("📡 Status HTTP: %s", response.status_code)
        logging.debug("📄 Resposta: %s", response.text)

        try:
            data = response.json()
        except json.JSONDecodeError:
            logging.error("❌ Resposta não é um JSON válido: %s", response.text)
            return 0.0

        if data.get("retCode") == 0:
            saldo = data["result"]["balance"][0]["transferBalance"]
            logging.info(f"💰 Saldo disponível na conta {conta}: {saldo} {moeda}")
            return float(saldo)
        else:
            logging.error(f"❌ Erro ao consultar saldo: {data}")
            return 0.0
    except requests.RequestException as e:
        logging.exception("❗ Falha na requisição de saldo: %s", str(e))
        return 0.0

def movimentar_para_funding(quantidade, moeda="USDC"):
    saldo_funding = consultar_saldo(moeda, "FUND")
    if saldo_funding >= quantidade:
        logging.info("✅ Já existe saldo suficiente na conta FUND. Nenhuma transferência necessária.")
        return

    timestamp = str(int(time.time() * 1000))
    request_id = str(uuid.uuid4()).replace("-", "")
    body = {
        "fromAccountType": "UNIFIED",
        "toAccountType": "FUND",
        "coin": moeda,
        "amount": str(quantidade),
        "transferId": request_id
    }
    body_str = json.dumps(body, separators=(",", ":"))
    payload = f"{timestamp}{BYBIT_API_KEY}5000{body_str}"
    assinatura = gerar_assinatura(BYBIT_API_SECRET, payload)

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-SIGN": assinatura,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": "5000",
        "X-BAPI-SIGN-TYPE": "2",
        "Content-Type": "application/json"
    }

    url = f"{BYBIT_BASE_URL}/v5/asset/transfer/inter-transfer"
    logging.info("🔄 Movendo fundos de UNIFIED para FUND...")
    try:
        response = requests.post(url, headers=headers, data=body_str)
        resposta = response.json()
        if resposta.get("retCode") != 0:
            logging.error("❌ Erro ao mover fundos: [%s] %s", resposta.get("retCode"), resposta.get("retMsg"))
        else:
            logging.info("✅ Movimentação concluída com sucesso: %s", resposta)
    except Exception as e:
        logging.exception("❗ Exceção ao mover fundos: %s", str(e))

def sacar_para_binance(valor, endereco_destino, moeda="USDC", rede="BSC"):
    saldo_funding = consultar_saldo(moeda, "FUND")
    if saldo_funding < valor:
        logging.error("❌ Saldo insuficiente na FUND para sacar.")
        return

    timestamp = str(int(time.time() * 1000))
    body = {
        "accountType": "FUND",
        "coin": moeda,
        "chain": rede,
        "address": endereco_destino,
        "amount": str(valor),
        "forceChain": 0,
        "timestamp": timestamp
    }
    body_str = json.dumps(body, separators=(",", ":"))
    payload = f"{timestamp}{BYBIT_API_KEY}5000{body_str}"
    assinatura = gerar_assinatura(BYBIT_API_SECRET, payload)

    headers = {
        "X-BAPI-API-KEY": BYBIT_API_KEY,
        "X-BAPI-SIGN": assinatura,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": "5000",
        "X-BAPI-SIGN-TYPE": "2",
        "Content-Type": "application/json"
    }

    url = f"{BYBIT_BASE_URL}/v5/asset/withdraw/create"
    logging.info(f"📤 Iniciando saque de {valor} {moeda} para Binance (rede {rede})...")
    try:
        response = requests.post(url, headers=headers, data=body_str)
        resposta = response.json()
        if resposta.get("retCode") != 0:
            logging.error("❌ Erro no saque: [%s] %s", resposta.get("retCode"), resposta.get("retMsg"))
        else:
            logging.info("✅ Saque solicitado com sucesso: %s", resposta)
    except Exception as e:
        logging.exception("❗ Exceção ao tentar sacar: %s", str(e))

def main():
    quantidade = 5
    endereco_binance = "0x789aca852cf967f06caff82448427dad8ab94a7b"
    rede = "BSC"

    movimentar_para_funding(quantidade)
    logging.info("⏳ Aguardando 5 segundos antes de iniciar o saque...")
    time.sleep(5)
    sacar_para_binance(quantidade, endereco_binance, rede=rede)

if __name__ == "__main__":
    main()


#PS C:\Users\user\Desktop\Git_Crypto\study> & c:/Users/user/Desktop/Git_Crypto/study/.venv/Scripts/python.exe c:/Users/user/Desktop/Git_Crypto/study/transferir_bybit_para_binance.py
#2025-04-08 17:32:13,005 - INFO - 💰 Saldo disponível na conta FUND: 10 USDC
#2025-04-08 17:32:13,006 - INFO - ✅ Já existe saldo suficiente na conta FUND. Nenhuma transferência necessária.
#2025-04-08 17:32:13,007 - INFO - ⏳ Aguardando 5 segundos antes de iniciar o saque...
#2025-04-08 17:32:18,330 - INFO - 💰 Saldo disponível na conta FUND: 10 USDC
#2025-04-08 17:32:18,332 - INFO - 📤 Iniciando saque de 5 USDC para Binance (rede BSC)...
#2025-04-08 17:32:18,944 - INFO - ✅ Saque solicitado com sucesso: {'retCode': 0, 'retMsg': 'success', 'result': {'id': '135545243'}, 'retExtInfo': 
#{}, 'time': 1744129938855}
#PS C:\Users\user\Desktop\Git_Crypto\study> 