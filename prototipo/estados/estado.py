from abc import ABC, abstractmethod


class Estado(ABC):
    def __init__(self):
        raise NotImplementedError("Estado não implementado")

    @abstractmethod
    def iniciar(self):
        raise NotImplementedError("Iniciar não implementado")

    @abstractmethod
    def atualizar(self, eventos, tempo_passado ):
        raise NotImplementedError("Atualizar não implementado")
