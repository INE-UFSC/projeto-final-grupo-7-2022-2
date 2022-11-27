import pygame as pg
import os
from configuracoes import Configuracoes



class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf):
        super().__init__()
        self.__config = Configuracoes()
        self.__image = pg.transform.scale(surf, (self.__config.tamanho_tile, self.__config.tamanho_tile))
        self.__rect = self.image.get_rect(topleft = pos)
        self.__hitbox = self.rect

    
    def atualizar(self, tempo_passado):
        pass

    def desenhar(self):
        return (self,)

    @property
    def config(self):
        return self.__config

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

    @property
    def hitbox(self):
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, hitbox):
        self.__hitbox = hitbox


# Uma especialização do tile, serve para representar estruturas maiores que o tamanho de um tile comum
class Estrutura(Tile):
    def __init__(self, pos, surf):
        super().__init__(pos, surf)

        self.rect = self.image.get_rect(midbottom = pos)
        self.rect.height = 22

# Outra especialização do tile, serve para representar o chão do mapa
class Chao(Tile):
    def __init__(self, width, height, pos, surf):
        super().__init__(pos, surf)
        self.image = pg.transform.scale(surf, (width * self.config.tamanho_tile, height * self.config.tamanho_tile))
