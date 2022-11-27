import pygame as pg
import pytmx
import os

from configuracoes import Configuracoes
from .tile import Tile, Estrutura, Chao

from entidades.jogador import Jogador
from entidades.ladino import Ladino
from entidades.guerreiro import Guerreiro
from entidades.arqueiro import Arqueiro

class FaseConstrutor():
    def __init__(self, fase, nome):

        self.__config = Configuracoes()
        self.__fase = fase
        self.__nome = nome

        # Carrega o arquivo .tmx
        tmx_path = os.path.join('./View/mapas', self.__nome, self.__nome + '.tmx')
        self.__data = pytmx.load_pygame(tmx_path, pixelalpha=True)

            
        self.__grupos = {
            'chao'      : self.__gerar_chao(),
            'blocos'    : self.__gerar_blocos(),
            'colisores' : self.__gerar_colisores(),
            # 'estruturas': self.__gerar_estruturas(),
            'entidades' : self.__gerar_entidades()
        }

    @property
    def data(self):
        return self.__data

    @property
    def grupos(self):
        return self.__grupos

    def __gerar_chao(self):
        floor_path = os.path.join('./View/mapas', self.__nome, 'floor.png')
        floor_surf = pg.image.load(floor_path).convert_alpha()
        height = self.__data.height
        width = self.__data.width

        return Chao(width, height, pos = (0, 0), surf = floor_surf)


    def __gerar_blocos(self) -> list:

        blocos = []
        for layer in self.__data.visible_layers:
            if hasattr(layer,'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * self.__config.tamanho_tile, y * self.__config.tamanho_tile)
                    blocos.append(Tile(pos = pos, surf = surf))

        return blocos

    def __gerar_colisores(self):

        colisores = []
        for layer in self.__data.layers:
            if hasattr(layer,'data'):
                if layer.name == 'collision' or layer.name == 'object_obstacles':
                    for x, y, surf in layer.tiles():
                        pos = (x * self.__config.tamanho_tile, y * self.__config.tamanho_tile)
                        colisores.append(Tile(pos = pos, surf = surf))

        return colisores

    def __gerar_estruturas(self):
        
        estruturas = []
        # Percorre o arquivo tmx e inlcui os objetos em seu respectivo grupo
        for estrutura in self.__data.objectgroups:
            pos = estrutura.x, estrutura.y
            estruturas.append(Estrutura(pos = pos, surf = estrutura.image))

        return estruturas

    def __gerar_entidades(self):

        entidades = []
        for group in self.__data.objectgroups:
            if group.name == 'entities':
                for entity in group:
                    if entity.name == 'player':
                        entidades.append(Jogador(self.__fase, (entity.x * 4, entity.y *4)))
                    elif entity.name == 'ladino':
                        pass
                    elif entity.name == 'guerreiro':
                        pass
                    elif entity.name == 'arqueiro':
                        pass

        return entidades
