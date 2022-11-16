from pygame import font as fonte
from os import path


class Singleton(object):
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance


class Configuracoes(Singleton):
    def __init__(self):
        self.__largura_tela = 1280
        self.__altura_tela = 720

        self.__volume_musica = None

        self.__tamanho_tile = 32
        self.__max_fps = 240
        self.__tps = 60

        fonte.init()
        self.__fonte_titulo = fonte.SysFont('Arial', 80)

    @property
    def fonte_titulo(self):
        return self.__fonte_titulo

    @property
    def tps(self):
        return self.__tps

    @property
    def max_fps(self):
        return self.__max_fps

    @property
    def tamanho_tile(self):
        return self.__tamanho_tile

    @property
    def largura_tela(self):
        return self.__largura_tela

    @property
    def altura_tela(self):
        return self.__altura_tela

    @property
    def volume_musica(self):
        return self.__volume_musica

    @volume_musica.setter
    def volume_musica(self, volume_musica):
        self.__volume_musica = volume_musica
