from .arma import Arma

class Pistola(Arma):
    def __init__(self):
        raise NotImplementedError("Pistola não implementada")

    @property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")

    def usar_arma(self):
        raise NotImplementedError("Usar arma não implementado")