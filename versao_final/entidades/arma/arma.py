from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

import pygame as pg

from visualizacao import SuperficiePosicionada
from utilidades import Configuracoes

if TYPE_CHECKING:
    from entidades import Jogador
    from fase import Fase


class Arma(ABC):
    def __init__(self, jogador: 'Jogador'):
        super().__init__()
        self.__configuracoes = Configuracoes()
        self._jogador = jogador
        self.__tipo = None
        self.__ativo = False

        self._direcao = None
        self._distancia = 0.5

        self._posicao = pg.Vector2(0, 0)

    def definir_fase(self, fase: 'Fase'):
        self._fase = fase

    @property
    def tipo(self) -> str:
        raise NotImplementedError('O método tipo() deve ser implementado')

    @property
    def ativo(self) -> bool:
        return self.__ativo

    @ativo.setter
    def ativo(self, ativo: bool):
        self.__ativo = ativo

    @abstractmethod
    def usar_arma(self) -> None:
        pass

    @abstractmethod
    def gerar_dict_do_estado(self) -> dict:
        pass

    def _atualizar_posicao_e_direcao(self, posicao_do_mouse_relativa_ao_jogador: pg.Vector2) -> None:
        if posicao_do_mouse_relativa_ao_jogador.magnitude() > 0:
            self._direcao = posicao_do_mouse_relativa_ao_jogador.normalize()
            vetor_jogador = pg.Vector2(self._jogador.rect.center)
            # Posição da arma
            vetor_posicao_da_arma = (vetor_jogador + (self._direcao * self._distancia * self.__configuracoes.tamanho_tile))
            self._posicao = (vetor_posicao_da_arma.x, vetor_posicao_da_arma.y)

    def atualizar(self, posicao_do_mouse_relativa_ao_jogador: pg.Vector2, tempo_passado: int) -> None:
        if self.ativo:
            self._atualizar_posicao_e_direcao(posicao_do_mouse_relativa_ao_jogador)

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        if self.ativo:
            angulo = 0
            if self._direcao is not None and self._direcao.magnitude() > 0:
                angulo = self._direcao.angle_to(pg.Vector2(1, 0))

            superficie = pg.transform.rotate(self._imagem, angulo)
            rect = superficie.get_rect(center=self._posicao)
            return (SuperficiePosicionada(superficie, rect.topleft),)
        return tuple()
