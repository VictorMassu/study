# simulador.py
from utils.logger import setup_logger
from utils.taxas import obter_taxas
from config import MARGEM_LUCRO_MINIMA_PORCENTO

logger = setup_logger()

def calcular_lucro(par, preco_compra, preco_venda, quantidade, origem, destino):
    taxas = obter_taxas(par, origem=origem, destino=destino)
    custo_total = preco_compra * quantidade
    custo_total += custo_total * (taxas['trading_origem'] / 100)
    custo_total += taxas['saque'] + taxas['custo_rede']

    valor_venda = preco_venda * quantidade
    valor_venda -= valor_venda * (taxas['trading_destino'] / 100)

    lucro = valor_venda - custo_total
    lucro_percentual = (lucro / custo_total) * 100 if custo_total > 0 else 0

    logger.info(f"[Simulação] {par} | {origem} -> {destino} | Lucro: {lucro:.4f} USDT ({lucro_percentual:.4f}%)")
    return lucro
