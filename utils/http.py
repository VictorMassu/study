# utils/http.py

import requests
import time
import logging

logger = logging.getLogger(__name__)

def safe_request(method, url, headers=None, params=None, data=None, retries=3, delay=2, timeout=10):
    """
    Faz uma requisição HTTP com tratamento de erros, tentativas e logs detalhados.

    Args:
        method (str): 'GET' ou 'POST'
        url (str): URL da requisição
        headers (dict): Cabeçalhos HTTP
        params (dict): Parâmetros de query string
        data (dict): Dados para POST
        retries (int): Número de tentativas
        delay (int): Tempo entre tentativas (s)
        timeout (int): Tempo limite da requisição (s)

    Returns:
        dict ou None: JSON da resposta ou None em caso de falha
    """
    for tentativa in range(1, retries + 1):
        try:
            logger.info(f"[HTTP] [{tentativa}/{retries}] Requisição {method.upper()} para {url}")
            inicio = time.time()

            if method.upper() == 'GET':
                resposta = requests.get(url, headers=headers, params=params, timeout=timeout)
            elif method.upper() == 'POST':
                resposta = requests.post(url, headers=headers, json=data, timeout=timeout)
            else:
                logger.error(f"[HTTP] Método inválido: {method}")
                return None

            duracao = time.time() - inicio
            logger.debug(f"[HTTP] Tempo da requisição: {duracao:.2f}s")

            if resposta.status_code == 200:
                logger.debug(f"[HTTP] Sucesso [{resposta.status_code}]: {url}")
                return resposta.json()
            else:
                logger.warning(
                    f"[HTTP] Status {resposta.status_code} ao acessar {url} - "
                    f"Resposta: {resposta.text}"
                )

        except requests.exceptions.RequestException as e:
            logger.exception(f"[HTTP] Erro ao acessar {url} na tentativa {tentativa}: {e}")

        time.sleep(delay)

    logger.error(f"[HTTP] Todas as tentativas falharam para URL: {url}")
    return None
