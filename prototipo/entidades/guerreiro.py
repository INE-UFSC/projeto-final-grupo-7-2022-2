from .entidade import Entidade


class Guerreiro(Entidade):
    def __init__(self):
        raise NotImplementedError("Guerreiro não implementado")

    @property
    def tipo(self):
        return "guerreiro"

    def atualizar(self, eventos: list):
        raise NotImplementedError("Atualizar não implementado")

    def desenhar(self):
        raise NotImplementedError("Desenhar não implementado")
