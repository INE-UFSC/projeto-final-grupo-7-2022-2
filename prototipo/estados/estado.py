from abc import ABC


class Estado(ABC):
    def __init__(self):
        raise NotImplementedError("Estado não implementado")

    def iniciar(self):
        raise NotImplementedError("Iniciar não implementado")
