from .entidade import Entidade


class Guerreiro(Entidade):
    def __init__(self):
        raise NotImplementedError("Guerreiro não implementado")

    def atualizar(self, eventos: list):
        raise NotImplementedError("Atualizar não implementado")

    def renderizar(self):
        raise NotImplementedError("Renderizar não implementado")
