from typing import TYPE_CHECKING

import pygame as pg

from .arma import Arma

if TYPE_CHECKING:
    from entidades import Jogador

from superficie_posicionada import SuperficiePosicionada


class Faca(Arma):
    def __init__(self, jogador: 'Jogador'):
        super().__init__(jogador)

        self.chegou_no_30 = False
        self.tipo_sprite = 'faca'

        self.__escala = (10, 10)
        self._imagem = pg.Surface(self.__escala)
        self._imagem.fill('red')
        # self.rect = self.image.get_rect(center = (0,0))

    @property
    def tipo(self) -> str:
        return 'faca'

    def usar_arma(self):

        if self.ativo:
            if not self.chegou_no_30:
                self._distancia += 5
                if self._distancia == 50:
                    self.chegou_no_30 = True
            else:
                self._distancia -= 5
                if self._distancia == 20:
                    self.ativo = False
                    self.chegou_no_30 = False

    def atualizar(self, posicao_do_mouse_relativa_ao_jogador: pg.Vector2, tempo_passado: int):
        super().atualizar(posicao_do_mouse_relativa_ao_jogador, tempo_passado)
