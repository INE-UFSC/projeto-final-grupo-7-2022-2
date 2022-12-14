from typing import Tuple

import pygame as pg

from utilidades import Configuracoes
from visualizacao import Spritesheet, SuperficiePosicionada

from .inimigo import Inimigo


class Ladino(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self._vida = 1
        self._velocidade = 0.9
        self._raio_ataque = 0.1
        self._raio_percepcao = 5

        self.__frame_indice = 0
        self.__status = 'right'
        self.__spritesheet = Spritesheet("ladino")
        self.__animacoes = self.__spritesheet.get_animation_frames()

        self._tempo_de_recarga_ataque = 1000
        self.__momento_ataque = 0

        # Movimento
        self._rect = self.__superficie_atual.get_rect()
        self._hitbox = self.rect.inflate(pg.Vector2(-0.5, -0.5) * self._configuracoes.tamanho_tile)

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

    def __atacar(self) -> None:
        dano = 10
        jogador = self._fase.jogador
        agora = pg.time.get_ticks()
        if self._hitbox.colliderect(jogador._hitbox) and agora > self.__momento_ataque + self._tempo_de_recarga_ataque:
            self.__momento_ataque = pg.time.get_ticks()
            jogador.receber_dano(dano)

    def atualizar(self, tempo_passado: int) -> None:
        direcao = self._calcular_vetor_diferenca_jogador()*-1
        super().atualizar(tempo_passado)
        self.__calcular_tipo_de_animacao(direcao)
        self.__animar()
        self.__atacar()

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        ladino_desenho = SuperficiePosicionada(self.__superficie_atual, self._rect.topleft)
        return (ladino_desenho,)
