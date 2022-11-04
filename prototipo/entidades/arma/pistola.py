import pygame as pg
from entidades.arma.bala import *
# from bala import Bala


class Pistola(pg.sprite.Sprite):
    def __init__(self, fase, groups) -> None:
        super().__init__(groups)

        self.__fase = fase
        self.__tipo_sprite = 'pistola'

        # Imagem
        self.image = pg.Surface((10, 10))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = (0, 0))

        # Capacidade
        self.__regarga = 6
        self.__tiros = []

        self.v_mouse = None
        self.posicao = None

    def tipo(self):
        return 'pistola'

    def mover(self, posicao_jogador: tuple, posicao_mouse: tuple):
        # Direção da arma e ajuste de posição com relação ao jogador
        self.v_mouse = pg.math.Vector2(posicao_mouse[0] - self.__fase.config.largura_tela // 2,
                                    posicao_mouse[1] - self.__fase.config.altura_tela // 2)

        self.direcao = self.v_mouse.normalize() * 20

        # Posição da arma
        self.posicao = (posicao_jogador[0] + self.direcao.x, posicao_jogador[1] + self.direcao.y)
        self.rect.x = self.posicao[0]
        self.rect.y = self.posicao[1]

    def atirar(self, posicao_mouse: tuple):
        if len(self.__tiros) <= self.__regarga:
            self.__tiros.append(Bala(self.__fase, [self.__fase.grupo_de_entidade, 
                                                self.__fase.attack_sprites], 
                                    self.posicao, self.v_mouse))

    def recarregar(self):
        self.__tiros.clear()

    def desenhar(self):
        return (self,)
    
    def atualizar(self, tempo):
        pass