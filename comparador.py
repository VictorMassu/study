from exchanges.registry import EXCHANGES
from utils.taxas import obter_taxas
from utils.lucro import calcular_lucro_real
import logging

logger = logging.getLogger(__name__)

def comparar_e_decidir(par_moeda, quantidade):
    """
    Compara todas as possíveis rotas de arbitragem entre exchanges disponíveis no registro,
    calcula o lucro real com taxas e decide se alguma rota deve ser executada.
    """
    melhores_opcao = {
        "lucro_percentual": -float('inf'),
        "origem": None,
        "destino": None,
        "lucro_usdt": 0,
        "preco_compra": 0,
        "preco_venda": 0,
        "executar": False
    }

    exchanges = list(EXCHANGES.keys())

    for origem in exchanges:
        for destino in exchanges:
            if origem == destino:
                continue  # evita auto-arbitragem

            logger.info(f"\n[Comparação] {origem} -> {destino} para {par_moeda}")

            preco_compra, _ = EXCHANGES[origem].obter_preco(par_moeda)
            _, preco_venda = EXCHANGES[destino].obter_preco(par_moeda)

            if preco_compra is None or preco_venda is None:
                logger.warning(f"Preços inválidos para rota {origem} -> {destino}")
                continue

            taxas = obter_taxas(par_moeda, origem, destino)

            resultado = calcular_lucro_real(
                preco_compra=preco_compra,
                preco_venda=preco_venda,
                quantidade=quantidade,
                taxa_trading_compra=taxas['trading_origem'],
                taxa_trading_venda=taxas['trading_destino'],
                taxa_saque=taxas['saque'],
                custo_rede_usdt=taxas['custo_rede']
            )

            logger.info(f"[Lucro] {origem} -> {destino} | Lucro: {resultado['lucro_usdt']} USDT ({resultado['lucro_percentual']}%)")

            if resultado['lucro_percentual'] > melhores_opcao['lucro_percentual']:
                melhores_opcao.update({
                    "lucro_percentual": resultado['lucro_percentual'],
                    "lucro_usdt": resultado['lucro_usdt'],
                    "origem": origem,
                    "destino": destino,
                    "preco_compra": preco_compra,
                    "preco_venda": preco_venda,
                    "executar": resultado['executar']
                })

    if melhores_opcao['executar']:
        logger.info(f"🚀 Executar arbitragem de {melhores_opcao['origem']} para {melhores_opcao['destino']}! Lucro: {melhores_opcao['lucro_percentual']}% ({melhores_opcao['lucro_usdt']} USDT)")
        # Aqui você pode integrar a execução real da arbitragem
    else:
        logger.info(f"⛔ Nenhuma rota vantajosa encontrada para {par_moeda}. Melhor lucro: {melhores_opcao['lucro_percentual']}%")
