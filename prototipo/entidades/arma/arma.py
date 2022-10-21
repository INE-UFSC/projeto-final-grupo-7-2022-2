from abc import ABC


class Arma(ABC):
    def __init__(self):
        raise NotImplementedError("Arma não implementada")

    @property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")

    def usar_arma(self):
        raise NotImplementedError("Usar arma não implementado")
