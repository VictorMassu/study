def obter_taxas(par, origem, destino):
    """
    Retorna as taxas de trading, saque e custo de rede entre duas exchanges.
    Args:
        par (str): Par de moedas, ex: BTC/USDT
        origem (str): Exchange de origem, ex: 'binance'
        destino (str): Exchange de destino, ex: 'bybit'
    Returns:
        dict: com as taxas
    """

    taxas_fixas = {
        "binance": 0.1,  # 0.1%
        "bybit": 0.1     # 0.1%
    }

    taxas_saque = {
        "USDT": 0.3,     # USDT por saque
        "BTC": 0.0005,
        "ETH": 0.005
    }

    custo_rede = {
        "default": 0.2  # custo estimado da rede (ex: Polygon ou BSC)
    }

    moeda = par.replace("USDT", "").strip()

    return {
        "trading_origem": taxas_fixas.get(origem, 0.1),
        "trading_destino": taxas_fixas.get(destino, 0.1),
        "saque": taxas_saque.get(moeda, 0.3),
        "custo_rede": custo_rede["default"]
    }
