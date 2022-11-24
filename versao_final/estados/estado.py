from abc import ABC, abstractmethod
from maquina_de_estado import MaquinaDeEstado


class Estado(ABC):
    def __init__(self, maquina_de_estado: MaquinaDeEstado):
        self.__maquina_de_estado = maquina_de_estado

    @property
    def maquina_de_estado(self):
        return self.__maquina_de_estado

    '''@abstractmethod
    def iniciar(self):
        raise NotImplementedError("Iniciar não implementado")'''

    @abstractmethod
    def atualizar(self, eventos: list, delta_time: float):
        pass
