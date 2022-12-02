from typing import TYPE_CHECKING, List, Callable

import pygame as pg

from callback_de_evento import CallbackDeEvento
from configuracoes import Configuracoes
from entidades import Jogador
from estados.estado import Estado
from fase import Fase

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class Partida(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__fases = []
        self.__fase_atual_indice = 0
        self.__tem_jogo = False
        self.__jogador = Jogador()

        self.__callback_de_eventos = []
        self.__idenficador_de_evento_indice = 0

        self.__tela = pg.display.get_surface()
        self.__configuracoes = Configuracoes()

    def registrar_evento(self, tipo: int, callback: Callable) -> int:
        identificador = self.__idenficador_de_evento_indice
        callback_de_evento = CallbackDeEvento(identificador, tipo, callback)
        self.__callback_de_eventos.append(callback_de_evento)
        self.__idenficador_de_evento_indice += 1
        return identificador

    def remover_registro_de_evento(self, identificador: int):
        for callback_de_evento in self.__callback_de_eventos:
            if callback_de_evento.id == identificador:
                self.__callback_de_eventos.remove(callback_de_evento)
                break

    def registrar_fase(self, fase: 'Fase'):
        self.__fases.append(fase)

    def jogo_perdido(self):
        self._maquina_de_estado.mover_para_estado('fim_de_jogo')
        self.__tem_jogo = False

    def terminar_fase(self):
        self.__fase_atual_indice += 1
        self.__callback_de_eventos = []
        if self.__fase_atual_indice >= len(self.__fases):
            self._maquina_de_estado.mover_para_estado('fim_de_jogo')
            self.__tem_jogo = False

    def desenhar(self):
        self.__tela.fill('black')
        self.__fases[self.__fase_atual_indice].desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: float):
        for evento in eventos:
            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                self._maquina_de_estado.mover_para_estado('menu_pausa')
            else:
                for callback_de_evento in self.__callback_de_eventos:
                    if evento.type == callback_de_evento.tipo:
                        callback_de_evento.disparar(evento)
        self.__fases[self.__fase_atual_indice].atualizar(tempo_passado)

    def iniciar(self):
        if not self.__tem_jogo:
            self.__fase_atual_indice = 0
            self.__fases[self.__fase_atual_indice].iniciar(jogador=self.__jogador)
            self.__tem_jogo = True
