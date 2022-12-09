from typing import TYPE_CHECKING, List, Callable

import pygame as pg

from controlador_de_musica import ControladorDeMusica
from callback_de_evento import CallbackDeEvento
from configuracoes import Configuracoes
from entidades import Jogador
from estados.estado import Estado
from fase import Fase
from View.transicao import Transicao

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class Partida(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__fases = []
        self.__fase_atual_indice = 0
        self.__tem_jogo = False
        self.__musica_control = ControladorDeMusica()
        self.__jogador = Jogador()
        self.__marcador_de_tempo_para_eventos = 0
        self.__callback_de_eventos = []
        self.__callback_eventos_de_tempo = []
        self.__idenficador_de_evento_indice = 0
        self.__tela = pg.display.get_surface()
        self.__configuracoes = Configuracoes()
        self.__transicao = Transicao()
        self.__ultimo_quadro_fase: pg.Surface | None = None
        self.__fase_ativa = True

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

    def iniciar_fase(self):
        self.__fases[self.__fase_atual_indice].iniciar(jogador=self.__jogador)

    def terminar_fase(self):
        self.__ultimo_quadro_fase = self.__tela.copy()
        self.__fase_ativa = False
        self.__callback_de_eventos = []

    def desenhar(self):
        self.__tela.fill('black')
        if self.__fase_ativa:
            self.__tela.blit(self.__fases[self.__fase_atual_indice].desenhar(), (0, 0))
            if not self.__transicao.terminou:
                self.__tela.blit(self.__transicao.desenhar(), (0, 0))
        else:
            if self.__ultimo_quadro_fase is not None:
                self.__tela.blit(self.__ultimo_quadro_fase, (0, 0))
                self.__tela.blit(self.__transicao.desenhar(), (0, 0))

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        if self.__fase_ativa:    
            self.__atualizar_fase(eventos, tempo_passado)
            if not self.__transicao.terminou:
                self.__transicao.atualizar(tempo_passado)   
        else:
            self.__transicao.atualizar(tempo_passado)
            if self.__transicao.iniciou:
                self.__fase_atual_indice += 1
                self.__fase_ativa = True
                if self.__fase_atual_indice >= len(self.__fases):
                        self._maquina_de_estado.mover_para_estado('fim_de_jogo')
                        self.__tem_jogo = False
                else:
                    self.iniciar_fase()
            

    def __atualizar_fase(self, eventos: List[pg.event.Event], tempo_passado: int):
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
                self.__fases[self.__fase_atual_indice].pausar_tempo()
            else:
                for callback_de_evento in self.__callback_de_eventos:
                    if evento.type == callback_de_evento.tipo:
                        callback_de_evento.disparar(evento)

    def iniciar(self):
        if not self.__tem_jogo:
            self.__fase_atual_indice = 0
            self.__fases[self.__fase_atual_indice].iniciar(jogador=self.__jogador)
            self.__tem_jogo = True
        self.__musica_control.parar_musica()
        self.__musica_control.iniciar_musica(self.__configuracoes.musica_jogo) 
