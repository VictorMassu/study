# exchanges/liquidez.py


from utils.logger import setup_logger

# Inicializa o logger
logger = setup_logger()

# Banco de liquidez global para monitorar o saldo de USDC e outras criptos nas exchanges
LIQUIDEZ = {
    "binance": {
        "USDC": 500.0,
        "BTC": 0
    },
    "bybit": {
        "USDC": 0.0,
        "BTC": 0.01
    }
}

# Função para verificar o saldo disponível em uma exchange e moeda específica
def verificar_liquidez(exchange, moeda):
    """
    Verifica se o saldo de uma moeda em uma exchange é suficiente para a operação.
    """
    if LIQUIDEZ[exchange][moeda] > 0:
        logger.info(f"[LIQUIDEZ] Saldo suficiente de {moeda} na {exchange}: {LIQUIDEZ[exchange][moeda]}")
        return True
    else:
        logger.warning(f"[LIQUIDEZ] Saldo insuficiente de {moeda} na {exchange}.")
        return False

# Função para atualizar o banco de liquidez após uma operação de compra ou venda
def atualizar_liquidez(exchange, moeda, quantidade, operacao):
    """
    Atualiza o banco de liquidez global após uma compra ou venda.
    - operacao: 'compra' ou 'venda'
    """
    if operacao == "compra":
        LIQUIDEZ[exchange][moeda] -= quantidade
    elif operacao == "venda":
        LIQUIDEZ[exchange][moeda] += quantidade
    logger.info(f"[LIQUIDEZ] Liquidez atualizada: {quantidade} {moeda} {operacao} na {exchange}. Novo saldo: {LIQUIDEZ[exchange][moeda]}")

# Função para aguardar liquidez suficiente na exchange antes de iniciar a operação
def aguardar_liquidez(exchange, moeda):
    """
    Aguarda até que a liquidez necessária esteja disponível para iniciar uma operação.
    """
    while not verificar_liquidez(exchange, moeda):
        logger.info(f"[LIQUIDEZ] Esperando liquidez suficiente na {exchange} para {moeda}...")
        time.sleep(10)  # Espera 10 segundos e tenta novamente
