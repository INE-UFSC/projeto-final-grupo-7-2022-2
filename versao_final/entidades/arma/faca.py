import pygame as pg
from .arma import Arma


class Faca(Arma):
    def __init__(self, fase):
        super().__init__(fase)
        
        self.fase = fase
        self.tipo = 'faca'
        self.chegou_no_30 = False
        self.tipo_sprite = 'faca'

        self.__escala = (10, 10)
        self.image  = pg.Surface(self.__escala)
        self.image.fill('red')
        # self.rect = self.image.get_rect(center = (0,0))


    def usar_arma(self):
        
        if self.ativo:
            if not self.chegou_no_30:
                self.distancia += 5
                if self.distancia == 50:
                    self.chegou_no_30 = True
            else:
                self.distancia -= 5
                if self.distancia == 20:
                    self.ativo = False
                    self.chegou_no_30 = False
                
    def atualizar(self, tempo):
        self.usar_arma()

