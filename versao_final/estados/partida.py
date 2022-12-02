from typing import TYPE_CHECKING, List

import pygame as pg

from callback_de_evento import CallbackDeEvento
from configuracoes import Configuracoes
from estados.estado import Estado
from fase import Fase

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class Partida(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__fases = []
        self.__fase_atual_indice = 0
        self.__callback_de_eventos = []
        self.__id_indice = 0

        self.__tela = pg.display.get_surface()
        self.__configuracoes = Configuracoes()

    def registrar_evento(self, tipo: int, callback: callable) -> int:
        identificador = self.__id_indice
        callback_de_evento = CallbackDeEvento(identificador, tipo, callback)
        self.__callback_de_eventos.append(callback_de_evento)
        self.__id_indice += 1
        return identificador

    def remover_registro_de_evento(self, id: int):
        for callback_de_evento in self.__callback_de_eventos:
            if callback_de_evento.id == id:
                self.__callback_de_eventos.remove(callback_de_evento)
                break

    def registrar_fase(self, fase: 'Fase'):
        self.__fases.append(fase)

    def terminar_fase(self):
        self.__fase_atual_indice += 1
        if self.__fase_atual_indice >= len(self.__fases):
            self._maquina_de_estado.mover_para_estado('fim_de_jogo')

    def desenhar(self):
        self.__tela.fill('black')
        self.__fases[self.__fase_atual_indice].desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: float):
        self.__fases[self.__fase_atual_indice].atualizar(tempo_passado)
        for evento in eventos:
            for callback_de_evento in self.__callback_de_eventos:
                if evento.type == callback_de_evento.tipo:
                    callback_de_evento.disparar(evento)

    def iniciar(self):
        self.__fase_atual_indice = 0
        self.__fases[self.__fase_atual_indice].iniciar()
