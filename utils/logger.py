
# logger.py
# Sistema de logs centralizado com criação automática da pasta "logs"

import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("logs/crypto_arbitragem.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("ArbitragemLogger")
