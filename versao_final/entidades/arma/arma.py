from abc import ABC, abstractmethod
import pygame as pg

class Arma(ABC, pg.sprite.Sprite):
    def __init__(self, fase, groups):
        super().__init__(groups)
        
        self.__fase = fase
        self.__tipo = None
        self.__ativo = False

        # Imagem
        # self.__spritesheet = spritesheet
        self.__image = pg.Surface((10,10))
        self.__rect = self.__image.get_rect(center = (1000000, 1000000))

        # Posicionamento
        self.__posicao = None
        self.__vetor = None
        self.__direcao = None
        self.__distancia = 20
    

    @property
    def fase(self):
        return self.__fase

    @fase.setter
    def fase(self, fase):
        self.__fase = fase

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        self.__tipo = tipo

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, ativo):
        self.__ativo = ativo

    @property	
    def posicao(self) -> tuple:
        return self.__posicao

    @property
    def direcao(self) -> tuple:
        return self.__direcao

    @property
    def vetor(self):
        return self.__vetor

    @property
    def distancia(self):
        return self.__distancia

    @distancia.setter
    def distancia(self, distancia):
        self.__distancia = distancia

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect


    @abstractmethod
    def usar_arma(self):
        pass

    def mover(self, posicao_jogador: tuple, posicao_mouse: tuple):
        # Direção da arma e ajuste de posição com relação ao jogador
        self.__vetor = pg.math.Vector2(posicao_mouse).normalize() * self.__distancia

        # Posição da arma
        self.__posicao = (posicao_jogador[0] + self.__vetor.x, posicao_jogador[1] + self.__vetor.y)
        self.rect.x = self.posicao[0]
        self.rect.y = self.posicao[1]

    def desenhar(self):
        return (self,)
