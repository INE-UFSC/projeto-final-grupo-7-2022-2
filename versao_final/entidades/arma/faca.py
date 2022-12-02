from typing import TYPE_CHECKING

import pygame as pg

from .arma import Arma

if TYPE_CHECKING:
    from entidades import Jogador

from superficie_posicionada import SuperficiePosicionada


class Faca(Arma):
    def __init__(self, jogador: 'Jogador', *args, **kwargs):
        super().__init__(jogador)

        self.__chegou_no_30 = kwargs.get('chegou_no_30', False)

        if 'distancia' in kwargs:
            self._distancia = kwargs['distancia']

        self.__tipo_sprite = 'faca'

        self.__escala = (10, 10)
        self._imagem = pg.Surface(self.__escala)
        self._imagem.fill('red')
        # self.rect = self.image.get_rect(center = (0,0))

    @staticmethod
    def apartir_do_dict(dados: dict, jogador: 'Jogador') -> 'Faca':
        return Faca(jogador, **dados)

    @property
    def tipo(self) -> str:
        return 'faca'

    def gerar_dict_do_estado(self) -> dict:
        return {
            'chegou_no_30': self.__chegou_no_30,
            'distancia': self._distancia
        }

    def usar_arma(self):

        if self.ativo:
            if not self.__chegou_no_30:
                self._distancia += 5
                if self._distancia == 50:
                    self.__chegou_no_30 = True
            else:
                self._distancia -= 5
                if self._distancia == 20:
                    self.ativo = False
                    self.__chegou_no_30 = False
