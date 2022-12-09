from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple
from configuracoes import Configuracoes

import pygame as pg

from .entidade import Entidade
from .jogador import Jogador

if TYPE_CHECKING:
    from fase import Fase


class Inimigo(Entidade):
    def __init__(self):
        super().__init__()

        self.__configuracoes = Configuracoes()
        self.status = 'right_idle'

        self._raio_ataque: int = None
        self._raio_limiar: int = 0.5
        self._raio_percepcao: int = None

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
        distancia = vetor_diferenca_jogador.magnitude() / self.__configuracoes.tamanho_tile
        if distancia != 0 and distancia < self._raio_percepcao:
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
        self._fase.matar_entidade(self)

    def atualizar(self, tempo_passado: int) -> None:
        vetor_diferenca_jogador = self._calcular_vetor_diferenca_jogador()
        self._acoes(vetor_diferenca_jogador)
        self._mover(tempo_passado)
