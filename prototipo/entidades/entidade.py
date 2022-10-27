from abc import ABC
import pygame as pg
from fase import Fase

class Entidade(ABC):
    def __init__(self) -> None:
        self.velocidade = None
        self.sprite = None
        self.sentido = None

    def registrar_na_fase(self, fase):
        raise NotImplementedError("Registrar na fase não implementado")

    @property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")

    def atualizar(self, delta: float):
        raise NotImplementedError("Atualizar não implementado")

    def renderizar(self, tela: pg.Surface):
        raise NotImplementedError("Renderizar não implementado")

    def receber_dano(self, dano: int):
        raise NotImplementedError("Receber dano não implementado")
