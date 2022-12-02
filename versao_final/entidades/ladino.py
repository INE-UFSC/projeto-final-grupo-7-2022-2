from typing import TYPE_CHECKING, Tuple

import pygame as pg

from configuracoes import Configuracoes
from spritesheet import Spritesheet
from superficie_posicionada import SuperficiePosicionada

from .entidade import Entidade
from .inimigo import Inimigo
from .jogador import Jogador

if TYPE_CHECKING:
    from fase import Fase


class Ladino(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self.velocidade = 4
        self._raio_ataque = 25
        self._raio_percepcao = 150

        configuracoes = Configuracoes()
        self._tempo_de_recarga_ataque = 10 * configuracoes.tps

        # Configurações de gráfico - Ainda estão provisórias
        self.__cor = (255, 0, 0)
        self.__image = pg.Surface((configuracoes.tamanho_tile, configuracoes.tamanho_tile))

        # Movimento
        self._rect = self.__image.get_rect()
        self._hitbox = self.rect.inflate(0, -10)

    @property
    def tipo(self) -> str:
        return "ladino"

    def __animar(self) -> None:
        self._rect = self.__image.get_rect(center=self.hitbox.center)

    def atualizar(self, tempo_passado: int) -> None:
        super().atualizar(tempo_passado)
        self.__animar()
        self._tempos_de_recarga()

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        return (SuperficiePosicionada(self.__image, self._rect.topleft),)
