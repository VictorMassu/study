# historico.py
# Salva o histórico de ordens executadas ou simuladas em um arquivo JSON

import json
import os
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger()

ARQUIVO_HISTORICO = "logs/historico_ordens.json"

def salvar_ordem(par, exchange, tipo_ordem, quantidade, preco, lucro_esperado, simulado=False, origem=None, destino=None):
    """
    Salva uma ordem (real ou simulada) no histórico em formato JSON.
    """
    ordem = {
        "data_hora": datetime.now().isoformat(),
        "par": par,
        "exchange": exchange,
        "tipo_ordem": tipo_ordem,
        "quantidade": quantidade,
        "preco": preco,
        "lucro_esperado": round(lucro_esperado, 2),
        "simulado": simulado,
        "origem": origem,
        "destino": destino
    }

    historico = []

    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r") as f:
                historico = json.load(f)
        except json.JSONDecodeError:
            logger.warning("Histórico anterior corrompido ou vazio. Criando novo.")

    historico.append(ordem)

    with open(ARQUIVO_HISTORICO, "w") as f:
        json.dump(historico, f, indent=4)

    logger.info(f"[HISTÓRICO] Ordem registrada: {ordem}")
