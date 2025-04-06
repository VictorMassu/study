
# main.py

from config import PARES, VALOR_POR_ORDEM_USDT, MODO_SIMULACAO
import config
from exchanges.binance import obter_preco_binance
from exchanges.bybit import obter_preco_bybit
from comparador import comparar_precos
from simulador import calcular_lucro
from executor_ordens import enviar_ordem_binance
from executor_ordens_bybit import enviar_ordem_bybit
from utils.logger import setup_logger
from historico import salvar_ordem
from utils.binance_utils import get_precision_binance



logger = setup_logger()

def rodar_analise():
    logger.info("Iniciando ciclo de análise de arbitragem")
    for par in PARES:
        logger.info(f"\n--- 🔍 Analisando par: {par} ---")
        preco_bnb = obter_preco_binance(par)
        preco_byb = obter_preco_bybit(par)

        if preco_bnb == (None, None) or preco_byb == (None, None):
            logger.warning(f"Preços inválidos para {par}, pulando análise.")
            continue

        logger.info(f"Binance - {par}: Compra {preco_bnb[0]}, Venda {preco_bnb[1]}")
        logger.info(f"Bybit   - {par}: Compra {preco_byb[0]}, Venda {preco_byb[1]}")
        
        comparar_precos(par, preco_bnb, preco_byb)

        if preco_bnb[0] < preco_byb[1]:
            logger.info(f"Oportunidade: Comprar na Binance, vender na Bybit")
            lucro = calcular_lucro(par, preco_bnb[0], preco_byb[1])
            if not MODO_SIMULACAO and lucro > 0:
                casas_decimais = get_precision_binance(par)
                quantidade = round(VALOR_POR_ORDEM_USDT / preco_bnb[0], casas_decimais)
                logger.info(f"Calculando ordem para {par} | Qtd: {quantidade} | Preço compra: {preco_bnb[0]} | Preço venda: {preco_byb[1]}")
                enviar_ordem_binance(par=par, side="BUY", quantidade=str(quantidade), preco=str(preco_bnb[0]))
                enviar_ordem_bybit(par=par, side="SELL", quantidade=str(quantidade), preco=str(preco_byb[1]))
                salvar_ordem(par, "Binance", "BUY", quantidade, preco_bnb[0], lucro)
                salvar_ordem(par, "Bybit", "SELL", quantidade, preco_byb[1], lucro)

        elif preco_byb[0] < preco_bnb[1]:
            logger.info(f"Oportunidade: Comprar na Bybit, vender na Binance")
            lucro = calcular_lucro(par, preco_byb[0], preco_bnb[1])
            if not MODO_SIMULACAO and lucro > 0:
                casas_decimais = get_precision_binance(par)
                quantidade = round(VALOR_POR_ORDEM_USDT / preco_byb, casas_decimais)
                logger.info(f"Calculando ordem para {par} | Qtd: {quantidade} | Preço compra: {preco_byb[0]} | Preço venda: {preco_bnb[1]}")
                enviar_ordem_bybit(par=par, side="BUY", quantidade=str(quantidade), preco=str(preco_byb[0]))
                enviar_ordem_binance(par=par, side="SELL", quantidade=str(quantidade), preco=str(preco_bnb[1]))
                salvar_ordem(par, "Bybit", "BUY", quantidade, preco_byb[0], lucro)
                salvar_ordem(par, "Binance", "SELL", quantidade, preco_bnb[1], lucro)

        else:
            logger.info(f"Nenhuma arbitragem lucrativa encontrada para {par}")
    logger.info("Ciclo de análise finalizado")

if __name__ == "__main__":
    rodar_analise()
