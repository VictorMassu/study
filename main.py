from config import PARES, VALOR_POR_ORDEM_USDT, MODO_SIMULACAO, MARGEM_LUCRO_MINIMA_PORCENTO
from exchanges.binance import obter_preco_binance, verificar_saldo_binance
from exchanges.bybit import obter_preco_bybit, verificar_saldo_bybit as saldo_bybit
from comparador import comparar_e_decidir
from simulador import calcular_lucro
from executor_ordens import enviar_ordem_binance
from executor_ordens_bybit import enviar_ordem_bybit
from utils.logger import setup_logger
from historico import salvar_ordem
from utils.binance_utils import get_precision_binance
from config import BYBIT_API_KEY, BYBIT_API_SECRET

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

        quantidade = round(VALOR_POR_ORDEM_USDT / preco_bnb[0], 6)
        comparar_e_decidir(par, quantidade)

        # Simula as duas rotas dinamicamente
        rotas = [
            {"origem": "binance", "destino": "bybit", "preco_compra": preco_bnb[0], "preco_venda": preco_byb[1]},
            {"origem": "bybit", "destino": "binance", "preco_compra": preco_byb[0], "preco_venda": preco_bnb[1]},
        ]

        for rota in rotas:
            quantidade = round(VALOR_POR_ORDEM_USDT / rota["preco_compra"], 6)
            lucro = calcular_lucro(par, rota["preco_compra"], rota["preco_venda"], quantidade, rota["origem"], rota["destino"])

            if not MODO_SIMULACAO and lucro > 0:
                logger.info(f"[Execução] Comprar na {rota['origem']} e vender na {rota['destino']} | {par} | Qtd: {quantidade}")
                # Aqui entraria a lógica de envio de ordem real com base na rota escolhida

    logger.info("Ciclo de análise finalizado")

if __name__ == "__main__":
    rodar_analise()
