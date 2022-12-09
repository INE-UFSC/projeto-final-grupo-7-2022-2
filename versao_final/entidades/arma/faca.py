from os import path
from typing import TYPE_CHECKING

import pygame as pg

from configuracoes import Configuracoes

from .arma import Arma

if TYPE_CHECKING:
    from entidades import Jogador

from superficie_posicionada import SuperficiePosicionada


class Faca(Arma):
    def __init__(self, jogador: 'Jogador', *args, **kwargs):
        super().__init__(jogador)

        self.__configuracoes = Configuracoes()
        self.__tamanho = pg.Vector2(16, 3) * self.__configuracoes.tamanho_tile * 0.04
        self._imagem = pg.transform.scale(pg.image.load(path.join('recursos', 'sprites', 'peixeira.png')), self.__tamanho)
        self._esta_em_ataque = False
        self.__chegou_no_fim = False
        self.__distancia_maxima = 2
        self.__distancia_minima = 0.5
        self._distancia = self.__distancia_minima
        self.__ja_atacou = False

    @staticmethod
    def apartir_do_dict(dados: dict, jogador: 'Jogador') -> 'Faca':
        return Faca(jogador, **dados)

    @property
    def tipo(self) -> str:
        return 'faca'

    def gerar_dict_do_estado(self) -> dict:
        return {

        }

    def usar_arma(self):
        if not self._esta_em_ataque:
            self._esta_em_ataque = True

    def atualizar(self, posicao_do_mouse_relativa_ao_jogador, tempo_passado):
        if self.ativo:
            if self._esta_em_ataque:
                if self.__chegou_no_fim:
                    self._distancia -= 0.5
                    if self._distancia <= self.__distancia_minima:
                        self._esta_em_ataque = False
                        self.__chegou_no_fim = False
                        self.__ja_atacou = False
                else:
                    self._distancia += 0.5
                    if self._distancia >= self.__distancia_maxima:
                        self.__chegou_no_fim = True
                if not self.__ja_atacou:
                    rect = self._imagem.get_rect(center=self._posicao)
                    for entidade in self._fase.entidades:
                        if entidade != self._jogador:
                            if entidade.hitbox.colliderect(rect):
                                entidade.receber_dano(1)
                                self.__ja_atacou = True
                                break

            if self._esta_em_ataque:
                self._atualizar_posicao_e_direcao(self._direcao)
            else:
                self._atualizar_posicao_e_direcao(posicao_do_mouse_relativa_ao_jogador)
