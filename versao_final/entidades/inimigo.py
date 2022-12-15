from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

import pygame as pg

from utilidades import Configuracoes

from .entidade import Entidade
from .jogador import Jogador

if TYPE_CHECKING:
    from fase import Fase


class Inimigo(Entidade):
    def __init__(self):
        super().__init__()

        self.status = 'right_idle'

        self._raio_ataque: int = None
        self._raio_limiar: int = 0.5
        self._raio_percepcao: int = None

        self.__foi_atacado: bool = False
        self.__velocidade_normal: float | None = None
        self._pode_atacar: bool = True
        self._tempo_de_recarga_ataque: int | None = None
        self._vida = 3

    def _ativar_ataque(self) -> None:
        self._pode_atacar = True

    def _calcular_vetor_diferenca_jogador(self) -> pg.Vector2:
        vetor_inimigo = pg.Vector2(self.rect.center)
        vetor_jogador = pg.Vector2(self._fase.jogador.rect.center)
        return vetor_inimigo - vetor_jogador

    def _acoes(self, vetor_diferenca_jogador: pg.Vector2) -> None:
        distancia = vetor_diferenca_jogador.magnitude() / self._configuracoes.tamanho_tile
        if distancia != 0 and distancia < self._raio_percepcao:
            if self.__foi_atacado:
                self._direcao = vetor_diferenca_jogador.normalize()
                self.__velocidade_normal = self._velocidade
                self._velocidade = 5
                self.__foi_atacado = False
            else:
                if self.__velocidade_normal is not None:
                    self._velocidade = self.__velocidade_normal
                    self.__velocidade_normal = None
                if distancia > self._raio_ataque - self._raio_limiar and distancia < self._raio_ataque + self._raio_limiar:
                    self._direcao = pg.Vector2(0, 0)
                elif distancia > self._raio_ataque:
                    self._direcao = (-vetor_diferenca_jogador).normalize()
                else:
                    self._direcao = vetor_diferenca_jogador.normalize()
        else:
            self._direcao = pg.Vector2(0, 0)

    def receber_dano(self, dano: int) -> None:
        self._vida -= dano
        if self._vida <= 0:
            self._fase.matar_entidade(self)
        self.__foi_atacado = True

    def atualizar(self, tempo_passado: int) -> None:
        vetor_diferenca_jogador = self._calcular_vetor_diferenca_jogador()
        self._acoes(vetor_diferenca_jogador)
        self._mover(tempo_passado)
