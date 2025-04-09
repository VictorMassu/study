import json
import os

CAMINHO_FALLBACK = "taxas_fallback.json"

# Função para carregar taxas salvas localmente
def carregar_taxas_fallback():
    if os.path.exists(CAMINHO_FALLBACK):
        with open(CAMINHO_FALLBACK, "r") as f:
            return json.load(f)
    return {}

# Carrega as taxas iniciais
TAXAS_CACHE = carregar_taxas_fallback()

def obter_taxas(par, origem, destino):
    """
    Retorna as taxas de trading, saque e custo de rede entre duas exchanges.
    Usa cache local (taxas_fallback.json) e pode ser expandido para consultar APIs reais.

    Args:
        par (str): Par de moedas (ex: BTCUSDT)
        origem (str): Nome da exchange origem
        destino (str): Nome da exchange destino

    Returns:
        dict: Taxas {'trading_origem', 'trading_destino', 'saque', 'custo_rede'}
    """

    # Extrai a moeda base (ex: BTC de BTCUSDT ou ETH de ETHUSDC)
    moeda = par.replace("USDT", "").replace("USDC", "").strip().upper()

    # Carregar taxas fixas da cache
    taxas_fixas = TAXAS_CACHE.get("trading", {})
    taxas_saque = TAXAS_CACHE.get("saque", {})
    custo_rede = TAXAS_CACHE.get("custo_rede", {}).get("default", 0.2)

    return {
        "trading_origem": taxas_fixas.get(origem, 0.1),
        "trading_destino": taxas_fixas.get(destino, 0.1),
        "saque": taxas_saque.get(moeda, 0.3),
        "custo_rede": custo_rede
    }

# Utilitário para atualizar o cache local manualmente (você pode rodar isso num script separado)
def salvar_taxas_cache(novas_taxas: dict):
    with open(CAMINHO_FALLBACK, "w") as f:
        json.dump(novas_taxas, f, indent=4)
    print("✔ Cache de taxas salvo com sucesso.")
