# 🤖 Crypto_Beta

Um robô de arbitragem de criptomoedas em Python que simula e executa ordens reais (em testnets) entre Binance e Bybit.

## ⚙️ Funcionalidades
- Conecta na Binance Testnet e Bybit Testnet
- Monitora pares BTC/USDT e ETH/USDT
- Detecta oportunidades de arbitragem com base no spread
- Calcula lucro líquido considerando taxas de saque e trading
- Executa ordens LIMIT reais nas testnets se `MODO_SIMULACAO = False`
- Gera logs detalhados para análise e debug

## 🚀 Como usar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Crypto_Beta.git
cd Crypto_Beta
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` com suas credenciais:
```env
# .env
BINANCE_API_KEY=xxx
BINANCE_API_SECRET=xxx
BYBIT_API_KEY=xxx
BYBIT_API_SECRET=xxx
```

4. Execute o projeto:
```bash
python main.py
```

## 🧠 Estrutura

```
Crypto_Beta/
├── config.py
├── main.py
├── comparador.py
├── simulador.py
├── taxas.py
├── executor_ordens.py
├── executor_ordens_bybit.py
├── exchanges/
│   ├── binance.py
│   └── bybit.py
├── utils/
│   └── logger.py
├── logs/
│   └── crypto_arbitragem.log
├── .env.example
├── .gitignore
└── README.md
```

---

**Desenvolvido com ❤️ e inteligência para arbitragem estratégica.**