import pygame as pg
import pytmx
from .tile import Tile, Estrutura, Chao
import os
from configuracoes import Configuracoes


class Mapa():
    def __init__(self, nome):

        self.__config = Configuracoes()
        self.__nome = nome

        # Carrega o arquivo .tmx
        tmx_path = os.path.join('./View/mapas', self.__nome, self.__nome + '.tmx')
        self.__data = pytmx.load_pygame(tmx_path, pixelalpha=True)

            
        self.__fase = {
            'floor': self.__gerar_chao(),
            'tiles': self.__gerar_tiles(),
            'colisores': self.__gerar_colisores(),
            'objetos': self.__gerar_estruturas()
        }

    @property
    def data(self):
        return self.__data

    @property
    def fase(self):
        return self.__fase

    def __gerar_chao(self):
        floor_path = os.path.join('./View/mapas', self.__nome, 'floor.png')
        floor_surf = pg.image.load(floor_path).convert_alpha()
        height = self.__data.height
        width = self.__data.width

        return Chao(width, height, pos = (0, 0), surf = floor_surf)


    def __gerar_tiles(self) -> list:

        tiles = []
        for layer in self.__data.visible_layers:
            if hasattr(layer,'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * self.__config.tamanho_tile, y * self.__config.tamanho_tile)
                    tiles.append(Tile(pos = pos, surf = surf))

        return tiles

    def __gerar_colisores(self):

        colisores = []
        for layer in self.__data.layers:
            if layer not in self.__data.visible_layers:
                if hasattr(layer,'data'):
                    if layer.name == 'collision' or layer.name == 'object_obstacles':
                        for x, y, surf in layer.tiles():
                            pos = (x * self.__config.tamanho_tile, y * self.__config.tamanho_tile)
                            colisores.append(Tile(pos = pos, surf = surf))

        return colisores

    def __gerar_estruturas(self):
        
        estruturas = []
        # Percorre o arquivo tmx e inlcui os objetos em seu respectivo grupo
        for estrutura in self.__data.objects:
            pos = estrutura.x, estrutura.y
            estruturas.append(Estrutura(pos = pos, surf = obj.image))

        return estruturas