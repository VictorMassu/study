import time
import hmac
import hashlib
import requests
import logging
from config import BINANCE_API_KEY, BINANCE_API_SECRET

# Configurações
BINANCE_BASE_URL = "https://api.binance.com"
MOEDA = "USDC"
REDE = "BSC"  # Rede BSC (BEP20)
ENDERECO_DESTINO = "0xb6da240a5f91a0778558bc19491b678b89c39e5c"
QUANTIDADE_TRANSFERENCIA = 10  # Mínimo exigido pela Binance para USDC

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def gerar_assinatura(query_string):
    return hmac.new(
        BINANCE_API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def consultar_saldo(moeda):
    logging.info(f"🔍 Consultando saldo de {moeda} na Binance...")
    timestamp = int(time.time() * 1000)
    query = f"timestamp={timestamp}"
    signature = gerar_assinatura(query)
    url = f"{BINANCE_BASE_URL}/api/v3/account?{query}&signature={signature}"
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    for asset in data["balances"]:
        if asset["asset"] == moeda:
            saldo = float(asset["free"])
            logging.info(f"💰 Saldo disponível de {moeda}: {saldo}")
            return saldo
    return 0.0

def realizar_transferencia(moeda, rede, endereco, quantidade):
    logging.info(f"📤 Enviando {quantidade} {moeda} para {endereco} na rede {rede}...")
    timestamp = int(time.time() * 1000)
    query = (
        f"coin={moeda}&amount={quantidade}&address={endereco}"
        f"&network={rede}&timestamp={timestamp}"
    )
    signature = gerar_assinatura(query)
    full_url = f"{BINANCE_BASE_URL}/sapi/v1/capital/withdraw/apply?{query}&signature={signature}"
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }

    logging.info(f"🌐 URL da requisição: {full_url}")
    response = requests.post(full_url, headers=headers)
    
    if response.status_code == 200:
        logging.info("✅ Transferência realizada com sucesso.")
        logging.info(f"Resposta: {response.json()}")
    else:
        logging.error(f"❌ Erro HTTP: {response.status_code} - {response.text}")

def main():
    try:
        saldo = consultar_saldo(MOEDA)
        if saldo < QUANTIDADE_TRANSFERENCIA:
            logging.warning(f"🚫 Saldo insuficiente. Você tem {saldo} {MOEDA} e o mínimo para saque é {QUANTIDADE_TRANSFERENCIA}.")
            return

        logging.info(f"⚠️ Deseja transferir {QUANTIDADE_TRANSFERENCIA} {MOEDA} para {ENDERECO_DESTINO} na rede {REDE}?")
        confirmacao = input("Digite 'sim' para confirmar: ").strip().lower()
        if confirmacao == "sim":
            realizar_transferencia(MOEDA, REDE, ENDERECO_DESTINO, QUANTIDADE_TRANSFERENCIA)
        else:
            logging.info("❌ Operação cancelada pelo usuário.")
    except Exception as e:
        logging.error(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()


#PS C:\Users\user\Desktop\Git_Crypto\study> & c:/Users/user/Desktop/Git_Crypto/study/.venv/Scripts/python.exe c:/Users/user/Desktop/Git_Crypto/study/transferir_usdt_binance_para_bybit.py
#2025-04-07 21:42:02,320 - INFO - 🔍 Consultando saldo de USDC na Binance...
#2025-04-07 21:42:02,688 - INFO - 💰 Saldo disponível de USDC: 19.49405141
#2025-04-07 21:42:02,689 - INFO - ⚠️ Deseja transferir 10 USDC para 0xb6da240a5f91a0778558bc19491b678b89c39e5c na rede BSC?
#Digite 'sim' para confirmar: sim
#2025-04-07 21:42:10,701 - INFO - 📤 Enviando 10 USDC para 0xb6da240a5f91a0778558bc19491b678b89c39e5c na rede BSC...
#2025-04-07 21:42:10,702 - INFO - 🌐 URL da requisição: https://api.binance.com/sapi/v1/capital/withdraw/apply?coin=USDC&amount=10&address=0xb6da240a5f91a0778558bc19491b678b89c39e5c&network=BSC&timestamp=1744058530701&signature=b02d029568945d1e16d25e95c40015aa02cd6f6ae71749bfa53c7dd75fb15195 
#2025-04-07 21:42:11,384 - INFO - ✅ Transferência realizada com sucesso.
#2025-04-07 21:42:11,385 - INFO - Resposta: {'id': '9a15e366d26c46ab8032f12e8d45e84d'}
#PS C:\Users\user\Desktop\Git_Crypto\study> 