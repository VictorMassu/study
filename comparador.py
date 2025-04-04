
# comparador.py

from utils.logger import setup_logger
logger = setup_logger()

def comparar_precos(par, preco_bnb, preco_byb):
    if None in preco_bnb or None in preco_byb:
        return

    compra_binance, venda_binance = preco_bnb
    compra_bybit, venda_bybit = preco_byb

    if compra_binance < venda_bybit:
        spread = venda_bybit - compra_binance
        logger.info(f"Oportunidade de arbitragem: COMPRAR na Binance por {compra_binance} e VENDER na Bybit por {venda_bybit} | Spread: {spread}")
    elif compra_bybit < venda_binance:
        spread = venda_binance - compra_bybit
        logger.info(f"Oportunidade de arbitragem: COMPRAR na Bybit por {compra_bybit} e VENDER na Binance por {venda_binance} | Spread: {spread}")
    else:
        logger.info("Nenhuma oportunidade de arbitragem identificada no momento.")
