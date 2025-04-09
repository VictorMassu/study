# taxas/tax_binance.py

def obter_taxas_binance():
    return {
        "trading": 0.1,  # Exemplo: Taxa de trading fixa de 0.1%
        "saque": {
            "BTC": 0.0005,  # Taxa de saque de BTC
            "ETH": 0.005,    # Taxa de saque de ETH
            "USDT": 0.3      # Taxa de saque de USDT
        },
        "custo_rede": {
            "default": 0.2    # Custo estimado da rede (ex: Polygon ou BSC)
        }
    }
