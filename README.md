Projeto de Arbitragem de Criptomoedas

Este projeto tem como objetivo desenvolver um sistema automatizado para identificar e executar oportunidades de arbitragem entre exchanges de criptomoedas, especificamente a Binance e a Bybit, utilizando as testnets para simulação segura.

Funcionalidades

🔍 Monitoramento de preços em tempo real nas exchanges Binance e Bybit

📊 Identificação de oportunidades de arbitragem com base no spread

📦 Execução de ordens LIMIT reais nas testnets (Binance e Bybit)

🧠 Simulação de lucros, considerando taxas de negociação e saque

🧾 Registro histórico detalhado de cada operação

🔒 Configuração segura via .env

Tecnologias Utilizadas

Python 3.9+

Requests para chamadas de API

dotenv para variáveis de ambiente seguras

Sistema de logs detalhado com logging

Instalação e Configuração

1. Clone o repositório

git clone https://github.com/VictorMassu/study.git
cd study

2. Crie e ative um ambiente virtual

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Configure o arquivo .env

Crie um arquivo .env com base no modelo abaixo (.env.example):

BINANCE_API_KEY=coloque_sua_chave_aqui
BINANCE_API_SECRET=coloque_seu_segredo_aqui
BYBIT_API_KEY=coloque_sua_chave_aqui
BYBIT_API_SECRET=coloque_seu_segredo_aqui

⚠️ Nunca compartilhe seu .env real publicamente.

Executando o Projeto

Para iniciar o ciclo de análise de arbitragem:

python main.py

O sistema irá:

Buscar preços de compra e venda nas testnets

Verificar oportunidades de arbitragem

Simular ou executar ordens reais nas testnets

Registrar histórico das ordens com log detalhado

Estrutura de Diretórios

study/
│
├── exchanges/         # Scripts específicos para Binance e Bybit
├── utils/             # Logger, helpers e calculadoras
├── executor_ordens.py # Execução real de ordens nas testnets
├── simulador.py       # Simulação de ordens e lucros
├── main.py            # Script principal
├── .env.example       # Modelo para variáveis de ambiente
├── requirements.txt   # Dependências do projeto
└── README.md          # Este arquivo

Logs

Os logs são salvos em:

logs/crypto_arbitragem.log

Você pode acompanhar os ciclos de análise, ordens enviadas, e possíveis erros.

Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

🔐 Importante:
Este projeto utiliza testnets. Para ambientes reais, você deverá alterar as URLs das APIs no arquivo config.py e validar cuidadosamente limites de saque, taxas e segurança.

💬 Dúvidas, sugestões ou contribuições? Fique à vontade para abrir uma issue ou pull request!

🚀 Projeto em desenvolvimento por Victor Massu — com suporte do ChatGPT.