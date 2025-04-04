
# simulador.py

from utils.logger import setup_logger
from taxas import obter_taxas_simuladas

logger = setup_logger()

def calcular_lucro(par, preco_compra, preco_venda):
    taxas = obter_taxas_simuladas()
    taxa_total = preco_compra * taxas['taxa_binance'] + preco_venda * taxas['taxa_bybit'] + taxas['taxa_saque']
    lucro_bruto = preco_venda - preco_compra
    lucro_liquido = lucro_bruto - taxa_total

    logger.info(f"[Simulação] {par} - Lucro Bruto: {lucro_bruto:.2f}, Taxas: {taxa_total:.2f}, Lucro Líquido: {lucro_liquido:.2f}")
    return lucro_liquido
