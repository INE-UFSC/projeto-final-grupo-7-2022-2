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
        self.__marcador_de_tempo_para_eventos = 0
        self.__callback_de_eventos = []
        self.__callback_eventos_de_tempo = []
        self.__idenficador_de_evento_indice = 0
        self.__tela = pg.display.get_surface()
        self.__configuracoes = Configuracoes()

    def registrar_evento(self, tipo: int, callback: Callable) -> int:
        identificador = self.__idenficador_de_evento_indice
        callback_de_evento = CallbackDeEvento(identificador, tipo, callback)
        self.__callback_de_eventos.append(callback_de_evento)
        self.__idenficador_de_evento_indice += 1
        return identificador

    def esperar_certo_tempo(self, tempo: int, callback: Callable) -> int:
        identificador = self.__idenficador_de_evento_indice
        tempo = tempo + self.__marcador_de_tempo_para_eventos
        self.__callback_eventos_de_tempo.append((identificador,
                                                 tempo,
                                                 callback))
        self.__idenficador_de_evento_indice += 1
        return identificador

    def cancelar_esperar_certo_tempo(self, identificador: int):
        for i, (id_, tempo, callback) in enumerate(self.__callback_eventos_de_tempo):
            if id_ == identificador:
                self.__callback_eventos_de_tempo.pop(i)
                break

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

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        self.__fases[self.__fase_atual_indice].atualizar(tempo_passado)
        if len(self.__callback_eventos_de_tempo) > 0:
            self.__marcador_de_tempo_para_eventos += tempo_passado
        else:
            self.__marcador_de_tempo_para_eventos = 0
        i = len(self.__callback_eventos_de_tempo) - 1
        while i >= 0:
            identifier, tempo, callback = self.__callback_eventos_de_tempo[i]
            if tempo <= self.__marcador_de_tempo_para_eventos:
                callback()
                self.__callback_eventos_de_tempo.pop(i)
            i -= 1
        for evento in eventos:
            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                self._maquina_de_estado.mover_para_estado('menu_pausa')
            else:
                for callback_de_evento in self.__callback_de_eventos:
                    if evento.type == callback_de_evento.tipo:
                        callback_de_evento.disparar(evento)

    def iniciar(self):
        if not self.__tem_jogo:
            self.__fase_atual_indice = 0
            self.__fases[self.__fase_atual_indice].iniciar(jogador=self.__jogador)
            self.__tem_jogo = True
