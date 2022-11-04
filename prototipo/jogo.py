from estados import Estado

import pygame as pg
import pygame.time as pg_time
import sys
from configuracoes import Configuracoes
from evento_tps import evento_TPS
from entidades.jogador import Jogador
from fase import Fase


class Jogo:
    def __init__(self):
        self.__configuracoes = Configuracoes()

        # Inicia o pygame e define a janela
        pg.init()
        self.__display = pg.display.set_mode((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        pg.display.set_caption('SUPER LAMPARINA ARFANTE')
        self.__estados = {}
        self.__estado_atual: Estado | None = None
        self.__estado_inicial: Estado | None = None
        """ Timer para controlar o FPS """
        self.__timer_fps = pg.time.Clock()
        self.__timer_tps = pg.time.Clock()
        pg_time.set_timer(evento_TPS, 1000 // self.__configuracoes.tps)

    def iniciar(self):
        eventos = []
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == evento_TPS.type:
                    self.__estado_atual.atualizar(eventos, self.__timer_tps.tick())
                    eventos = []
                else:
                    eventos.append(event)

            self.__estado_atual.desenhar()
            pg.display.update()
            self.__timer_fps.tick(self.__configuracoes.max_fps)

    @property
    def estado_inicio(self):
        return self.__estado_inicial

    @estado_inicio.setter
    def estado_inicio(self, estado_inicio):
        self.__estado_inicial = estado_inicio

    def adicionar_estado(self, rotulo: str, estado: 'Estado'):
        self.__estados[rotulo] = estado
        if len(self.__estados) == 1 and self.__estado_inicial is None:
            self.__estado_inicial = rotulo

    def mover_para_estado(self, rotulo: str):
        self.__estado_atual = self.__estados[rotulo]
