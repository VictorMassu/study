# main.py

from config import PARES, VALOR_POR_ORDEM_USDC, MODO_SIMULACAO, MARGEM_LUCRO_MINIMA_PORCENTO
from exchanges.registry import EXCHANGES  # Registro dinâmico das exchanges
from exchanges.liquidez import verificar_liquidez, aguardar_liquidez, atualizar_liquidez
from comparador import comparar_e_decidir
from simulador import calcular_lucro
from utils.logger import setup_logger
from historico import salvar_ordem

logger = setup_logger()

def rodar_analise():
    logger.info("Iniciando ciclo de análise de arbitragem")

    for par in PARES:
        logger.info(f"\n--- 🔍 Analisando par: {par} ---")

        # Verificar se o par é válido nas exchanges antes de obter o preço
        for exchange_name, exchange in EXCHANGES.items():
            if par not in exchange.obter_pares_validos():
                logger.warning(f"Par {par} não é válido na {exchange_name}. Pulando análise.")
                continue

        # Obtendo preços das exchanges
        preco_exchanges = {}
        for exchange_name, exchange in EXCHANGES.items():
            preco_exchanges[exchange_name] = exchange.obter_preco(par)
            if preco_exchanges[exchange_name] == (None, None):
                logger.warning(f"Preços inválidos para {par} na {exchange_name}, pulando análise.")
                continue
            logger.info(f"{exchange_name} - {par}: Compra {preco_exchanges[exchange_name][0]}, Venda {preco_exchanges[exchange_name][1]}")

        # Encontrar as rotas de arbitragem
        rotas = []
        for origem in EXCHANGES:
            for destino in EXCHANGES:
                if origem != destino:
                    rotas.append({
                        "origem": origem,
                        "destino": destino,
                        "preco_compra": preco_exchanges[origem][0],
                        "preco_venda": preco_exchanges[destino][1]
                    })

        melhor_lucro = float("-inf")
        melhor_rota = None

        for rota in rotas:
            logger.info(f"\n[Análise de Rota] {rota['origem']} -> {rota['destino']} ({par})")

            if rota["preco_compra"] is None or rota["preco_venda"] is None:
                continue  # Pular rota inválida

            # Calcular quantidade estimada para arbitragem
            quantidade = round(VALOR_POR_ORDEM_USDC / rota["preco_compra"], 6)
            logger.info(f"Qtd estimada para arbitragem: {quantidade} {par.replace('USDT', '')}")

            # Calcular lucro da arbitragem
            lucro = calcular_lucro(par, rota["preco_compra"], rota["preco_venda"], quantidade, rota["origem"], rota["destino"])

            salvar_ordem(
                par=par,
                exchange=rota["origem"],
                tipo_ordem="SIMULACAO",
                quantidade=quantidade,
                preco=rota["preco_compra"],
                lucro_esperado=lucro,
                simulado=True,
                origem=rota["origem"],
                destino=rota["destino"]
            )

            if lucro > melhor_lucro:
                melhor_lucro = lucro
                melhor_rota = rota.copy()
                melhor_rota["lucro"] = lucro
                melhor_rota["quantidade"] = quantidade

        if melhor_lucro >= (VALOR_POR_ORDEM_USDC * (MARGEM_LUCRO_MINIMA_PORCENTO / 100)):
            logger.info(f"🚀 Executando arbitragem: {melhor_rota['origem']} -> {melhor_rota['destino']} com lucro: {melhor_rota['lucro']:.4f} USDT")

            if not MODO_SIMULACAO:
                origem_exchange = EXCHANGES[melhor_rota["origem"]]
                destino_exchange = EXCHANGES[melhor_rota["destino"]]

                # Verificar liquidez antes de enviar ordens
                if aguardar_liquidez(melhor_rota["origem"], "USDC"):
                    saldo_origem = origem_exchange.verificar_saldo("USDC")

                    if saldo_origem >= VALOR_POR_ORDEM_USDC:
                        # Enviar ordem de compra
                        compra = origem_exchange.enviar_ordem(
                            par=par,
                            side="BUY",
                            quantidade=melhor_rota["quantidade"],
                            preco=melhor_rota["preco_compra"]
                        )

                        if compra:
                            salvar_ordem(
                                par=par,
                                exchange=melhor_rota["origem"],
                                tipo_ordem="BUY",
                                quantidade=melhor_rota["quantidade"],
                                preco=melhor_rota["preco_compra"],
                                lucro_esperado=melhor_rota["lucro"],
                                simulado=False,
                                origem=melhor_rota["origem"],
                                destino=melhor_rota["destino"]
                            )

                            # Atualizar liquidez após a compra
                            atualizar_liquidez(melhor_rota["origem"], "USDC", melhor_rota["quantidade"], "compra")

                            # Enviar ordem de venda
                            venda = destino_exchange.enviar_ordem(
                                par=par,
                                side="SELL",
                                quantidade=melhor_rota["quantidade"],
                                preco=melhor_rota["preco_venda"]
                            )

                            if venda:
                                salvar_ordem(
                                    par=par,
                                    exchange=melhor_rota["destino"],
                                    tipo_ordem="SELL",
                                    quantidade=melhor_rota["quantidade"],
                                    preco=melhor_rota["preco_venda"],
                                    lucro_esperado=melhor_rota["lucro"],
                                    simulado=False,
                                    origem=melhor_rota["origem"],
                                    destino=melhor_rota["destino"]
                                )

                                # Atualizar liquidez após a venda
                                atualizar_liquidez(melhor_rota["destino"], "USDC", melhor_rota["quantidade"], "venda")
                            else:
                                logger.warning("[ARBITRAGEM] Ordem de venda falhou.")
                        else:
                            logger.warning("[ARBITRAGEM] Ordem de compra falhou.")
                    else:
                        logger.warning("[ARBITRAGEM] Saldo insuficiente para realizar arbitragem.")
                else:
                    logger.warning("[ARBITRAGEM] Liquidez insuficiente na origem.")
        else:
            porcentagem = (melhor_lucro / VALOR_POR_ORDEM_USDC) * 100
            logger.info(f"⛔ Nenhuma oportunidade de arbitragem viável encontrada. Melhor lucro: {porcentagem:.4f}%")

    logger.info("Ciclo de análise finalizado")

if __name__ == "__main__":
    rodar_analise()