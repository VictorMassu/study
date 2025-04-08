# exchanges/base.py

class ExchangeBase:
    def obter_preco(self, par):
        raise NotImplementedError("Método obter_preco() não implementado")

    def verificar_saldo(self, moeda):
        raise NotImplementedError("Método verificar_saldo() não implementado")

    def enviar_ordem(self, par, side, quantidade, preco):
        raise NotImplementedError("Método enviar_ordem() não implementado")
