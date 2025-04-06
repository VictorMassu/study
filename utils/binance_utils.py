# utils/binance_utils.py

import requests
from utils.logger import setup_logger

logger = setup_logger()

def get_precision_binance(symbol):
    try:
        url = "https://testnet.binance.vision/api/v3/exchangeInfo"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for s in data["symbols"]:
            if s["symbol"] == symbol:
                for f in s["filters"]:
                    if f["filterType"] == "LOT_SIZE":
                        step_size = float(f["stepSize"])
                        step_str = "{0:.10f}".format(step_size)
                        if "." in step_str:
                            precision = len(step_str.split(".")[1].rstrip("0"))
                        else:
                            precision = 0
                        logger.info(f"[Binance] Precisão do par {symbol}: {precision} casas decimais")
                        return precision
        logger.warning(f"[Binance] Precisão não encontrada para {symbol}, usando padrão 6")
        return 6
    except Exception as e:
        logger.error(f"Erro ao obter precisão para {symbol}: {e}")
        return 6
