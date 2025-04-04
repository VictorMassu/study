
# config.py
# Configurações globais do sistema de arbitragem

MODO_SIMULACAO = False  # Altere para False para enviar ordens reais nas testnets
VALOR_POR_ORDEM_USDT = 500.00  # Valor fixo por operação em USDT

# Pares monitorados
PARES = ["BTCUSDT", "ETHUSDT"]

# URLs das APIs de Testnet
BINANCE_BASE_URL = "https://testnet.binance.vision/api"
BYBIT_BASE_URL = "https://api-testnet.bybit.com"

# Credenciais de API (serão carregadas do .env)
import os
from dotenv import load_dotenv
load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

