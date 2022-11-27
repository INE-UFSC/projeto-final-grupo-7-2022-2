import pygame as pg
from entidades.arma.bala import *
from entidades.arma.arma import Arma


class Pistola(Arma):
    def __init__(self, fase) -> None:
        super().__init__(fase)

        # Identicadores
        self.fase = fase
        self.tipo = 'pistola'

        # Imagem
        self.image = pg.Surface((10, 10))
        self.image.fill('blue')
        # self.rect = self.image.get_rect(center = (0, 0))

        # Capacidade
        self.__regarga = 6
        self.__tiros = []


    def usar_arma(self):
        if len(self.__tiros) <= self.__regarga:
            self.__tiros.append(Bala(
                                self.fase,
                                self.posicao, self.vetor))

    def recarregar(self):
        self.__tiros.clear()

    def atualizar(self, tempo):
        pass