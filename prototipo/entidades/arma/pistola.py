import pygame as pg
from entidades.arma.bala import *
#from .arma import Arma

class Pistola():
    def __init__(self):
        #super().__init__(groups)
        self.__escala = (14, 6)
        self.__image = pg.image.load("sprites/Faca.png").convert_alpha()
        self.__image = pg.transform.scale(self.__image, self.__escala)
        #self.__rect = self.__image.get_rect(center = player.recte.center)
        self.__tiros = []

    '''@property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")'''

    def usar_arma(self, screen, x, y, escala, sentido):
        print(sentido)
        
        self.__tiros.append(Bala(x, y))
        for tiro in self.__tiros:
            tiro.atirar(sentido, screen, escala)
            if not tiro.ativo:
                self.__tiros.remove(tiro)