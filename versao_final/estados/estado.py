from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

import pygame as pg

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class Estado(ABC):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        self._maquina_de_estado = maquina_de_estado

    def iniciar(self):
        pass

    @abstractmethod
    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        pass
