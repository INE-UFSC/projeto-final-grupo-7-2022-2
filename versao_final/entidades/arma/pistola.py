from os import path
from typing import TYPE_CHECKING, List, Tuple

import pygame as pg

from utilidades import Configuracoes, ControladorDeMusica
from visualizacao import SuperficiePosicionada

from .arma import Arma
from .bala import Bala

if TYPE_CHECKING:
    from entidades import Jogador
    from fase import Fase



class Pistola(Arma):
    def __init__(self, jogador: 'Jogador', *args, **kwargs) -> None:
        super().__init__(jogador)
        self.__configuracoes = Configuracoes()
        self.__controle_de_musica = ControladorDeMusica()
        tamanho = pg.Vector2(16, 8) * self.__configuracoes.tamanho_tile * 0.05
        self._imagem = pg.transform.scale(pg.image.load(path.join('recursos', 'sprites', 'pistola.png')), tamanho)
        # Capacidade
        self.__regarga = 6
        self.__balas_restantes = kwargs.get('balas_restantes', self.__regarga)
        self.__tiros: List[Bala] = []

    @staticmethod
    def apartir_do_dict(dados: dict, jogador: 'Jogador') -> 'Pistola':
        return Pistola(jogador, **dados)

    @property
    def tipo(self) -> str:
        return 'pistola'

    @property
    def balas_restantes(self) -> int:
        return self.__balas_restantes

    def gerar_dict_do_estado(self) -> dict:
        return {
            'balas_restantes': self.__balas_restantes,
        }

    def definir_fase(self, fase: 'Fase'):
        super().definir_fase(fase)
        self.__tiros = []

    def usar_arma(self) -> None:
        if self.__balas_restantes > 0:
            self.__balas_restantes -= 1
            bala = Bala(self._fase, self._posicao, self._direcao)
            self.__tiros.append(bala)
            self.__controle_de_musica.som_ataque("pistola")

    def recarregar(self) -> None:
        self.__balas_restantes = self.__regarga

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        desenhos = super().desenhar()
        for tiro in self.__tiros:
            desenhos += tiro.desenhar()

        return desenhos

    def __atualizar_balas(self, tempo_passado: int) -> None:
        tiros_que_ainda_nao_terminaram = []
        for tiro in self.__tiros:
            chegou_ao_fim = tiro.atualizar(tempo_passado)
            if not chegou_ao_fim:
                tiros_que_ainda_nao_terminaram.append(tiro)
        self.__tiros = tiros_que_ainda_nao_terminaram

    def atualizar(self, posicao_do_mouse_relativa_ao_jogador: pg.Vector2, tempo_passado: int) -> None:
        super().atualizar(posicao_do_mouse_relativa_ao_jogador, tempo_passado)
        self.__atualizar_balas(tempo_passado)
