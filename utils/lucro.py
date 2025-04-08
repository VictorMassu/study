from config import MARGEM_LUCRO_MINIMA_PORCENTO

def calcular_lucro_real(preco_compra, preco_venda, quantidade,
                        taxa_trading_compra, taxa_trading_venda,
                        taxa_saque, custo_rede_usdt):
    """
    Calcula o lucro líquido percentual após taxas e custos operacionais.

    Args:
        preco_compra (float): Preço de compra na Exchange A
        preco_venda (float): Preço de venda na Exchange B
        quantidade (float): Quantidade da moeda (ex: USDT)
        taxa_trading_compra (float): % da taxa de trading na exchange de compra (ex: 0.1)
        taxa_trading_venda (float): % da taxa de trading na exchange de venda (ex: 0.1)
        taxa_saque (float): Quantidade em USDT cobrada na exchange de origem para saque
        custo_rede_usdt (float): Custo estimado da rede (ex: 0.2 USDT)

    Returns:
        dict: {'lucro_percentual': float, 'lucro_usdt': float, 'executar': bool}
    """

    # Total investido incluindo taxas e custos
    custo_total = preco_compra * quantidade
    custo_total += custo_total * (taxa_trading_compra / 100)
    custo_total += taxa_saque + custo_rede_usdt

    # Total recebido após venda
    valor_venda = preco_venda * quantidade
    valor_venda -= valor_venda * (taxa_trading_venda / 100)

    lucro_usdt = valor_venda - custo_total
    lucro_percentual = (lucro_usdt / custo_total) * 100 if custo_total > 0 else 0.0

    return {
        "lucro_percentual": round(lucro_percentual, 4),
        "lucro_usdt": round(lucro_usdt, 4),
        "executar": lucro_percentual >= MARGEM_LUCRO_MINIMA_PORCENTO
    }
