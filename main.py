from config import PARES, VALOR_POR_ORDEM_USDC, MODO_SIMULACAO
from exchanges.registry import EXCHANGES
from exchanges.liquidez import verificar_liquidez, aguardar_liquidez, atualizar_liquidez
from utils.estrategias import avaliar_estrategia
from utils.logger import setup_logger
from historico import salvar_ordem

logger = setup_logger()

def rodar_analise():
    logger.info("Iniciando ciclo de análise de arbitragem")

    for par in PARES:
        logger.info(f"\n--- 🔍 Analisando par: {par} ---")

        # Obter preços de compra e venda das exchanges
        preco_exchanges = {}
        for exchange_name, exchange in EXCHANGES.items():
            preco = exchange.obter_preco(par)
            preco_exchanges[exchange_name] = preco
            if preco != (None, None):
                logger.info(f"{exchange_name} - {par}: Compra {preco[0]}, Venda {preco[1]}")
            else:
                logger.warning(f"Preços inválidos para {par} na {exchange_name}, pulando análise.")

        # Criar todas as rotas possíveis
        rotas = []
        for origem in EXCHANGES:
            for destino in EXCHANGES:
                if origem != destino:
                    rotas.append({
                        "par": par,
                        "origem": origem,
                        "destino": destino,
                        "preco_compra": preco_exchanges[origem][0],
                        "preco_venda": preco_exchanges[destino][1]
                    })

        melhor_lucro = float("-inf")
        melhor_rota = None

        # Avaliar todas as rotas com base na estratégia
        for rota in rotas:
            logger.info(f"\n[Análise de Rota] {rota['origem']} -> {rota['destino']} ({par})")

            resultado = avaliar_estrategia(
                par=rota["par"],
                preco_compra=rota["preco_compra"],
                preco_venda=rota["preco_venda"],
                origem=rota["origem"],
                destino=rota["destino"]
            )

            if resultado["quantidade"] == 0:
                continue

            logger.info(f"Qtd estimada para arbitragem: {resultado['quantidade']} {par.replace('USDT', '')}")
            logger.info(f"[Simulação] {par} | {rota['origem']} -> {rota['destino']} | "
                        f"Lucro: {resultado['lucro_usdt']:.4f} USDT ({resultado['lucro_percentual']:.4f}%)")

            salvar_ordem(
                par=par,
                exchange=rota["origem"],
                tipo_ordem="SIMULACAO",
                quantidade=resultado["quantidade"],
                preco=rota["preco_compra"],
                lucro_esperado=resultado["lucro_usdt"],
                simulado=True,
                origem=rota["origem"],
                destino=rota["destino"]
            )

            if resultado["executar"] and resultado["lucro_usdt"] > melhor_lucro:
                melhor_lucro = resultado["lucro_usdt"]
                melhor_rota = rota.copy()
                melhor_rota.update(resultado)

        # Executar a melhor arbitragem (se houver)
        if melhor_rota and melhor_rota["executar"]:
            logger.info(f"🚀 Executando arbitragem: {melhor_rota['origem']} -> {melhor_rota['destino']} com lucro: {melhor_rota['lucro_usdt']:.4f} USDT")

            if not MODO_SIMULACAO:
                origem_exchange = EXCHANGES[melhor_rota["origem"]]
                destino_exchange = EXCHANGES[melhor_rota["destino"]]

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
                                lucro_esperado=melhor_rota["lucro_usdt"],
                                simulado=False,
                                origem=melhor_rota["origem"],
                                destino=melhor_rota["destino"]
                            )

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
                                    lucro_esperado=melhor_rota["lucro_usdt"],
                                    simulado=False,
                                    origem=melhor_rota["origem"],
                                    destino=melhor_rota["destino"]
                                )

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
