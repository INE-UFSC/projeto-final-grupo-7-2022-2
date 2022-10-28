import csv
from configuracoes import Configuracoes
import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.__configuracoes = Configuracoes()

        self.image = pg.transform.scale(pg.image.load('sprites/bloco_parede.png').convert_alpha(), (self.__configuracoes.tamanhotile, self.__configuracoes.tamanhotile))
        self.rect = self.image.get_rect(topleft = pos)

#Lê o arquivo .csv e organiza as informações em uma lista
class Mapa(pg.sprite.Sprite):
    def __init__(self, arquivocsv):
        self.mapa = []
        with open(arquivocsv, 'r') as file:
            file = csv.reader(file)
            for row in file:
                self.mapa.append(row)
