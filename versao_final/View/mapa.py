import pygame as pg
import pytmx
from .tile import Tile
import os


class Mapa():
    def __init__(self, nome, fase):
        # Carrega o arquivo .tmx
        file_path = os.path.join('./View/mapas', nome, 'data/tmx/', nome + '.tmx')
        self.__data = pytmx.load_pygame(file_path, pixelalpha=True)

        self.__fase = fase


    @property
    def data(self):
        return self.__data

    def gerar_mapa(self) -> list:
        mapa = []

        for layer in self.__data.visible_layers:
            if hasattr(layer,'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    Tile([self.__fase.camera], pos = pos, surf = surf)
                
        return mapa

    def gerar_colisores(self):
        # Percorre o arquivo tmx e inlcui os tiles invisíveis no seu respectivo grupo
        for layer in self.__data.invisible_layers:
            if hasattr(layer,'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 128, y * 128)
                    Tile(pos = pos, surf = surf)

    def gerar_objetos(self):
        # Percorre o arquivo tmx e inlcui os objetos em seu respectivo grupo
        for obj in self.__data.objects:
            pos = obj.x, obj.y
            Tile(pos = pos, surf = obj.image)