import os

import pygame as pg

from utilidades import Configuracoes

from .superficie_posicionada import SuperficiePosicionada


class Tile(SuperficiePosicionada):
    """  Tile é uma classe que representa um tile do mapa.

    Args:
        posicao (Vector2): Posição do tile no mapa.
        superficie (Surface): Superfície do tile.
        largura (int, optional): Largura do tile. O padrão é definido nas configurações. Nào pode ser zero ou negativo.
        altura (int, optional): Altura do tile. O padrão é definido nas configurações. Não pode ser zero ou negativo.
    """

    def __init__(self, posicao, superficie, largura: int = None, altura: int = None):
        configuracoes = Configuracoes()

        if largura is None or largura <= 0:
            largura = configuracoes.tamanho_tile

        if altura is None or altura <= 0:
            altura = configuracoes.tamanho_tile

        superficie_transformada = pg.transform.scale(superficie, (largura, altura))
        super().__init__(superficie_transformada, posicao)
