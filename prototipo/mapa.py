import csv
from configuracoes import Configuracoes
import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, fase, pos, groups):
        super().__init__(groups)
        self.__configuracoes = Configuracoes()

        self.image = pg.transform.scale(pg.image.load('sprites/bloco_parede.png').convert_alpha(), (self.__configuracoes.tamanho_tile, self.__configuracoes.tamanho_tile))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -4)
    
    def atualizar(self, tempo_passado):
        pass
    
    @property
    def tipo(self):
        return "tile"

    def desenhar(self):
        return (self,)
#Lê o arquivo .csv e organiza as informações em uma lista
class Mapa(pg.sprite.Sprite):
    def __init__(self, arquivocsv):
        self.mapa = []
        with open(arquivocsv, 'r') as file:
            file = csv.reader(file)
            for row in file:
                self.mapa.append(row)
