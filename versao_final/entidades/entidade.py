from abc import ABC
from math import sin
from typing import TYPE_CHECKING, Tuple

import pygame as pg

from superficie_posicionada import SuperficiePosicionada

if TYPE_CHECKING:
    from fase import Fase


class Entidade():
    def __init__(self) -> None:
        super().__init__()
        self._velocidade = 0
        self._direcao = pg.Vector2()

        self.frame_index = 0
        self._velocidade_da_animacao = 0.15

    @property
    def rect(self) -> pg.Rect:
        return self._rect

    @property
    def hitbox(self):
        return self._hitbox

    def registrar_na_fase(self, fase: 'Fase'):
        self._fase: 'Fase' = fase

    def definir_posicao(self, posicao: pg.Vector2) -> None:
        self.hitbox.x = posicao.x
        self.hitbox.y = posicao.y
        self._rect.center = self.hitbox.center

    def _mover(self, tempo_passado: int):
        if self._direcao.magnitude() != 0:
            self._direcao = self._direcao.normalize() * tempo_passado / 10

            # Realiza o movimento e checa a existência de colisões com a hitbox
            self.hitbox.x += self._direcao.x * self._velocidade
            self._calcular_colisao('horizontal')
            self.hitbox.y += self._direcao.y * self._velocidade
            self._calcular_colisao('vertical')
            self.rect.center = self.hitbox.center

    def _calcular_colisao(self, direcao: pg.Vector2):
        if direcao == 'horizontal':
            for colisor in self._fase.colisores:
                if colisor.rect.colliderect(self.hitbox):
                    if self._direcao.x > 0:
                        self.hitbox.right = colisor.rect.left
                    if self._direcao.x < 0:
                        self.hitbox.left = colisor.rect.right

        if direcao == 'vertical':
            for colisor in self._fase.colisores:
                if colisor.rect.colliderect(self.hitbox):
                    if self._direcao.y > 0:
                        self.hitbox.bottom = colisor.rect.top
                    if self._direcao.y < 0:
                        self.hitbox.top = colisor.rect.bottom

    # Função usada para oscilar a visibilidade com base no seno
    def wave_value(self) -> float:
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    @property
    def tipo(self) -> str:
        raise NotImplementedError(f"Tipo não implementado no tipo {self.tipo}")

    def atualizar(self, tempo_passado: int):
        raise NotImplementedError(f"Atualizar não implementado no tipo {self.tipo}")

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        raise NotImplementedError(f"Desenhar não implementado no tipo {self.tipo}")

    def receber_dano(self, dano: int) -> None:
        raise NotImplementedError(f"Receber dano não implementado no tipo {self.tipo}")
