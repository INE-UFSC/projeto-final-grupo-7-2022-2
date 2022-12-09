from typing import Tuple

import pygame as pg

from configuracoes import Configuracoes
from spritesheet import Spritesheet
from superficie_posicionada import SuperficiePosicionada

from .inimigo import Inimigo


class Ladino(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self._velocidade = 4
        self._raio_ataque = 0.1
        self._raio_percepcao = 5
        self.__frame_indice = 0
        self.__status = 'right'
        self.__spritesheet = Spritesheet("ladino")
        self.__animacoes = self.__spritesheet.get_animation_frames()

        configuracoes = Configuracoes()
        self._tempo_de_recarga_ataque = 10 * configuracoes.tps

        # Configurações de gráfico - Ainda estão provisórias
        self.__superficie = pg.Surface((configuracoes.tamanho_tile, configuracoes.tamanho_tile))

        # Movimento
        self._rect = self.__superficie.get_rect()
        self._hitbox = self.rect.inflate(0, -8)

    @property
    def tipo(self) -> str:
        return "ladino"

    @property
    def __superficie_atual(self):
        return self.__animacoes[self.__status][int(self.__frame_indice)]

    def __calcular_tipo_de_animacao(self, posicao_do_jogador: pg.Vector2) -> str:

        # Orientação do personagem com relação ao mouse
        if posicao_do_jogador.x > 0:
            self.__status = 'right'
        else:
            self.__status = 'left'
        # Animação de movimento
        if self._direcao.x == 0 and self._direcao.y == 0:
            self.__status += '_idle'

    def __animar(self) -> None:
        animacao = self.__animacoes[self.__status]

        self.__frame_indice += self._velocidade_da_animacao
        if self.__frame_indice >= len(animacao):
            self.__frame_indice = 0

    def atualizar(self, tempo_passado: int) -> None:
        direcao = self._calcular_vetor_diferenca_jogador()*-1
        super().atualizar(tempo_passado)
        self.__calcular_tipo_de_animacao(direcao)
        self.__animar()

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        ladino_desenho = SuperficiePosicionada(self.__superficie_atual, self._rect.topleft)
        return (ladino_desenho,)
