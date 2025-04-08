from dotenv import load_dotenv
import os

load_dotenv()

AMBIENTE = os.getenv("AMBIENTE", "prod").lower()

if AMBIENTE == "test":
    BINANCE_API_KEY = os.getenv("BINANCE_TEST_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_TEST_API_SECRET")
    BYBIT_API_KEY = os.getenv("BYBIT_TEST_API_KEY")
    BYBIT_API_SECRET = os.getenv("BYBIT_TEST_API_SECRET")
    BINANCE_BASE_URL = "https://testnet.binance.vision/api"
    BYBIT_BASE_URL = "https://api-testnet.bybit.com"
    MODO_SIMULACAO = True
else:
    BINANCE_API_KEY = os.getenv("BINANCE_PROD_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_PROD_API_SECRET")
    BYBIT_API_KEY = os.getenv("BYBIT_PROD_API_KEY")
    BYBIT_API_SECRET = os.getenv("BYBIT_PROD_API_SECRET")
    BINANCE_BASE_URL = "https://api.binance.com/api"
    BYBIT_BASE_URL = "https://api.bybit.com"
    MODO_SIMULACAO = False

# Parâmetros gerais
PARES = ["BTCEUR", "ETHEUR", "BTCUSDC", "ETHUSDC"]
VALOR_POR_ORDEM_USDC = 500.00
MARGEM_LUCRO_MINIMA_PORCENTO = 3.0
