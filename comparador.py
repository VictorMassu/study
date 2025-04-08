from exchanges import binance, bybit
from utils.taxas import obter_taxas
from utils.lucro import calcular_lucro_real


# Exemplo de função comparadora entre duas exchanges
def comparar_e_decidir(par_moeda, quantidade):
    exchanges = {
        "binance": {
            "obter_preco": binance.obter_preco_binance
        },
        "bybit": {
            "obter_preco": bybit.obter_preco_bybit
        }
    }
    melhores_opcao = {
        "lucro_percentual": -float('inf'),
        "origem": None,
        "destino": None,
        "lucro_usdt": 0,
        "preco_compra": 0,
        "preco_venda": 0
    }

    # Comparar todos os caminhos de arbitragem possíveis entre as exchanges
    for origem_nome, origem_api in exchanges.items():
        for destino_nome, destino_api in exchanges.items():
            if origem_nome == destino_nome:
                continue

            preco_compra = exchanges[origem_nome]["obter_preco"](par_moeda)[0]
            preco_venda = exchanges[destino_nome]["obter_preco"](par_moeda)[1]

            taxas = obter_taxas(par_moeda, origem=origem_nome, destino=destino_nome)

            resultado = calcular_lucro_real(
                preco_compra=preco_compra,
                preco_venda=preco_venda,
                quantidade=quantidade,
                taxa_trading_compra=taxas['trading_origem'],
                taxa_trading_venda=taxas['trading_destino'],
                taxa_saque=taxas['saque'],
                custo_rede_usdt=taxas['custo_rede']
            )

            if resultado['lucro_percentual'] > melhores_opcao['lucro_percentual']:
                melhores_opcao.update({
                    "lucro_percentual": resultado['lucro_percentual'],
                    "lucro_usdt": resultado['lucro_usdt'],
                    "origem": origem_nome,
                    "destino": destino_nome,
                    "preco_compra": preco_compra,
                    "preco_venda": preco_venda,
                    "executar": resultado['executar']
                })

    if melhores_opcao['executar']:
        print(f"🚀 Executar arbitragem de {melhores_opcao['origem']} para {melhores_opcao['destino']}! Lucro: {melhores_opcao['lucro_percentual']}% ({melhores_opcao['lucro_usdt']} USDT)")
        # Aqui você pode chamar a execução real
    else:
        print(f"⛔ Nenhuma oportunidade de arbitragem viável encontrada. Melhor lucro: {melhores_opcao['lucro_percentual']}%")
