from .entidade import Entidade


class Ladino(Entidade):
    def __init__(self):
        raise NotImplementedError("Ladino não implementado")

    def atualizar(self, eventos: list):
        raise NotImplementedError("Atualizar não implementado")

    def renderizar(self):
        raise NotImplementedError("Renderizar não implementado")
