import pygame as pg


class SuperficiePosicionada():
    def __init__(self, superficie: pg.Surface, topo_esquerdo: pg.Vector2) -> None:
        self.__superficie = superficie
        self.__rect = self.__superficie.get_rect(topleft=topo_esquerdo)

    @property
    def posicao(self) -> pg.Vector2:
        return self.__rect.topleft

    @posicao.setter
    def posicao(self, topo_esquerdo: pg.Vector2):
        self.__rect.topleft = topo_esquerdo

    @property
    def rect(self) -> pg.Rect:
        return self.__rect

    @property
    def superficie(self) -> pg.Surface:
        return self.__superficie

    @superficie.setter
    def superficie(self, superficie: pg.Surface):
        self.__superficie = superficie
