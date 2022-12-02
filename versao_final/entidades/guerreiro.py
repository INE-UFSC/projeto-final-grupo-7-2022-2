from typing import Tuple

import pygame as pg

from configuracoes import Configuracoes
from spritesheet import Spritesheet
from superficie_posicionada import SuperficiePosicionada

from .entidade import Entidade
from .inimigo import Inimigo


class Guerreiro(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self.velocidade = 2
        self._raio_ataque = 20
        self._raio_percepcao = 300
        self._vida = 3

        configuracoes = Configuracoes()
        self._tempo_de_recarga_ataque = 6 * configuracoes.tps

        # Configurações de gráfico - Ainda estão provisórias
        self.__cor = (255, 255, 0)
        self.__image = pg.Surface((configuracoes.tamanho_tile, configuracoes.tamanho_tile))
        self.__image.fill(self.__cor)

        # Movimento
        self._rect = self.__image.get_rect()
        self._hitbox = self.rect.inflate(0, -10)

    @property
    def tipo(self) -> str:
        return "guerreiro"

    def __animar(self) -> None:
        pass

    def atualizar(self, tempo_passado: int) -> None:
        super().atualizar(tempo_passado)
        self.__animar()
        self._tempos_de_recarga()

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        return (SuperficiePosicionada(self.__image, self._rect.topleft),)
