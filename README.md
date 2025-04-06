# 🤖 Crypto Arbitrage Bot (Testnet)

Este projeto é um robô de arbitragem automatizado entre as exchanges **Binance** e **Bybit**, utilizando as APIs **oficiais de testnet**.

Ele detecta oportunidades de lucro comprando cripto em uma exchange e vendendo em outra, tudo com execução de **ordens reais (LIMIT)** nas testnets.

---

## 🚀 Funcionalidades

✅ Consulta de preços ao vivo (Binance e Bybit)  
✅ Cálculo de spread e lucro real (com taxas)  
✅ Execução automática de ordens `LIMIT` nas testnets  
✅ Cálculo automático de quantidade com base em valor disponível (ex: 500 USDT)  
✅ Precisão dinâmica (casas decimais ajustadas por par)  
✅ Logs organizados e históricos salvos  
✅ Módulos organizados e prontos para escalar

---

## ⚙️ Requisitos

- Python 3.9 ou superior  
- Conta nas testnets da Binance e Bybit  
- Variáveis `.env` configuradas (veja `.env.example`)  
- Criação de par `logs/` para armazenar o log do bot

---

## 🛠️ Como usar

```bash
git clone https://github.com/VictorMassu/study.git
cd study
python -m venv .venv
source .venv/Scripts/activate  # (ou .venv/bin/activate no Linux/mac)
pip install -r requirements.txt
cp .env.example .env  # e preencha com suas chaves
python main.py
