# estrategias.py

from utils.taxas import obter_taxas
from utils.lucro import calcular_lucro_real
from config import VALOR_POR_ORDEM_USDC

def avaliar_estrategia(par, preco_compra, preco_venda, origem, destino):
    """
    Avalia se a arbitragem entre duas exchanges deve ser executada.
    
    Args:
        par (str): Par de moedas (ex: BTCUSDT)
        preco_compra (float): Preço de compra na exchange de origem
        preco_venda (float): Preço de venda na exchange de destino
        origem (str): Nome da exchange de origem
        destino (str): Nome da exchange de destino

    Returns:
        dict: {
            'lucro_usdt': float,
            'lucro_percentual': float,
            'executar': bool,
            'quantidade': float
        }
    """
    if preco_compra is None or preco_venda is None:
        return {
            'executar': False,
            'lucro_usdt': 0.0,
            'lucro_percentual': 0.0,
            'quantidade': 0.0
        }

    # Calcular quantidade baseada no valor por ordem
    quantidade = round(VALOR_POR_ORDEM_USDC / preco_compra, 6)

    # Obter taxas entre as exchanges
    taxas = obter_taxas(par, origem, destino)

    # Calcular lucro real
    resultado = calcular_lucro_real(
        preco_compra=preco_compra,
        preco_venda=preco_venda,
        quantidade=quantidade,
        taxa_trading_compra=taxas["trading_origem"],
        taxa_trading_venda=taxas["trading_destino"],
        taxa_saque=taxas["saque"],
        custo_rede_usdt=taxas["custo_rede"]
    )

    return {
        "lucro_usdt": resultado["lucro_usdt"],
        "lucro_percentual": resultado["lucro_percentual"],
        "executar": resultado["executar"],
        "quantidade": quantidade
    }
