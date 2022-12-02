from typing import Tuple, List

import pygame as pg

from configuracoes import Configuracoes
from spritesheet import Spritesheet
from superficie_posicionada import SuperficiePosicionada

from .entidade import Entidade
from .flecha import Flecha
from .inimigo import Inimigo


class Arqueiro(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self.velocidade = 0
        self._raio_ataque = 200
        self._raio_percepcao = 300
        self._vida = 1

        configuracoes = Configuracoes()
        self._tempo_de_recarga_ataque = 20 * configuracoes.tps
        self.__flechas: List[Flecha] = []

        # Configurações de gráfico - Ainda estão provisórias
        self.__cor = (255, 0, 255)
        self.__image = pg.Surface((configuracoes.tamanho_tile, configuracoes.tamanho_tile))
        self.__image.fill(self.__cor)

        # Movimento
        self._rect = self.__image.get_rect()
        self._hitbox = self.rect.inflate(0, -10)

    @property
    def tipo(self) -> str:
        return "arqueiro"

    def __atirar(self) -> None:
        if self._pode_atacar:
            vetor_diferenca = self._calcular_vetor_diferenca_jogador()
            if vetor_diferenca.magnitude() != 0:
                flecha = Flecha(self._fase, self._rect.center, vetor_diferenca)
                self.__flechas.append(flecha)
                self._pode_atacar = False

    def __atualizar_flechas(self, tempo_passado: int) -> None:
        flechas_que_ainda_nao_terminaram: List[Flecha] = []
        for flecha in self.__flechas:
            chegou_ao_fim = flecha.atualizar(tempo_passado)
            if not chegou_ao_fim:
                flechas_que_ainda_nao_terminaram.append(flecha)
        self.__flechas = flechas_que_ainda_nao_terminaram

    def atualizar(self, tempo_passado: int) -> None:
        super().atualizar(tempo_passado)
        self._tempos_de_recarga()
        self.__atirar()
        self.__atualizar_flechas(tempo_passado)

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        arqueiro_superficies = (SuperficiePosicionada(self.__image, self._rect.topleft),)
        for flecha in self.__flechas:
            arqueiro_superficies += flecha.desenhar()

        return arqueiro_superficies
