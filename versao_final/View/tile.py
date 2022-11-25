import pygame as pg
import os
from configuracoes import Configuracoes


class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        # self.__configuracoes = Configuracoes()
        # self.__tile_size = (self.__configuracoes.tamanho_tile)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

    
    def atualizar(self, tempo_passado):
        pass

    def desenhar(self):
        return (self,)
