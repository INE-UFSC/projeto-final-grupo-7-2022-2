from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

import pygame as pg

from .entidade import Entidade
from .jogador import Jogador

if TYPE_CHECKING:
    from fase import Fase


class Inimigo(Entidade):
    def __init__(self):
        super().__init__()

        self.status = 'right_idle'

        self._raio_ataque: int = None
        self._raio_percepcao: int = None

        self._pode_atacar: bool = True
        self._tempo_ataque: int | None = None
        self._tempo_de_recarga_ataque: int | None = None
        self._vida = 3

    def _obter_status(self, vetor_diferenca_jogador: pg.Vector2) -> None:
        # Pega a distância do player e o inimigo
        distancia = vetor_diferenca_jogador.magnitude()

        if distancia <= self._raio_ataque and self._pode_atacar:
            if self.status != 'attack':
                self.status = 'attack'
        elif distancia <= self._raio_percepcao:
            self.status = 'move'
        else:
            self.status = 'right_idle'

    def _tempos_de_recarga(self):
        tempo_atual = pg.time.get_ticks()
        if not self._pode_atacar and self._tempo_ataque is not None:
            if tempo_atual - self._tempo_ataque >= self._tempo_de_recarga_ataque:
                self._pode_atacar = True

    def _calcular_vetor_diferenca_jogador(self) -> pg.Vector2:
        vetor_inimigo = pg.Vector2(self.rect.center)
        vetor_jogador = pg.Vector2(self._fase.jogador.rect.center)
        return vetor_inimigo - vetor_jogador

    def _acoes(self, vetor_diferenca_jogador: pg.Vector2) -> None:
        if self.status == 'attack':
            self.tempo_ataque = pg.time.get_ticks()
            # ajeitar
            # self.dano_no_jogador()
            self.pode_atacar = False
        elif self.status == 'move':
            if vetor_diferenca_jogador.magnitude() != 0:
                self._direcao = (-vetor_diferenca_jogador).normalize()
        else:
            self._direcao = pg.Vector2()

    def receber_dano(self, dano: int) -> None:
        self._vida -= dano
        self._fase.matar_entidade(self)

    def atualizar(self, tempo_passado: int) -> None:
        vetor_diferenca_jogador = self._calcular_vetor_diferenca_jogador()
        self._obter_status(vetor_diferenca_jogador)
        self._acoes(vetor_diferenca_jogador)
        self._mover(tempo_passado)
