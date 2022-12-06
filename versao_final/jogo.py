import sys

import pygame as pg
import pygame.time as pg_time

from configuracoes import Configuracoes
from estados import (FimDeJogo, MenuCreditos, MenuOpcoes, MenuPrincipal, MenuRanking, MenuPausa, MenuRegistro, MenuVitoria, Partida)
from evento_tps import evento_TPS
from fase import Fase
from maquina_de_estado import MaquinaDeEstado


class Jogo:
    def __init__(self):
        pg.init()

        self.__maquina_de_estado = MaquinaDeEstado()
        self.__configuracoes = Configuracoes()

        self.__tela = pg.display.set_mode((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        pg.display.set_caption('SUPER LAMPARINA ARFANTE')

        self.__timer_fps = pg.time.Clock()
        self.__timer_tps = pg.time.Clock()
        pg_time.set_timer(evento_TPS, 1000 // self.__configuracoes.tps)

    def iniciar(self):
        partida = Partida(self.__maquina_de_estado)
        menu_principal = MenuPrincipal(self.__maquina_de_estado)
        menu_ranking = MenuRanking(self.__maquina_de_estado)
        menu_registro = MenuRegistro(self.__maquina_de_estado)
        menu_creditos = MenuCreditos(self.__maquina_de_estado)
        menu_opcoes = MenuOpcoes(self.__maquina_de_estado)
        menu_pausa = MenuPausa(self.__maquina_de_estado)
        fim_de_jogo = FimDeJogo(self.__maquina_de_estado)
        menu_vitoria = MenuVitoria(self.__maquina_de_estado)

        for fase in self.__configuracoes.fases:
            partida.registrar_fase(Fase(partida, fase))

        self.__maquina_de_estado.adicionar_estado("menu_principal", menu_principal)
        self.__maquina_de_estado.adicionar_estado("partida", partida)
        self.__maquina_de_estado.adicionar_estado("menu_ranking", menu_ranking)
        self.__maquina_de_estado.adicionar_estado("menu_registro", menu_registro)
        self.__maquina_de_estado.adicionar_estado("menu_creditos", menu_creditos)
        self.__maquina_de_estado.adicionar_estado("menu_opcoes", menu_opcoes)
        self.__maquina_de_estado.adicionar_estado("fim_de_jogo", fim_de_jogo)
        self.__maquina_de_estado.adicionar_estado("menu_pausa", menu_pausa)
        self.__maquina_de_estado.adicionar_estado("menu_vitoria", menu_vitoria)

        self.__maquina_de_estado.mover_para_estado("menu_principal")

        eventos = []
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == evento_TPS.type:
                    self.__maquina_de_estado.estado_atual.atualizar(eventos, self.__timer_tps.tick())
                    eventos = []
                else:
                    eventos.append(event)

            self.__maquina_de_estado.estado_atual.desenhar()
            pg.display.update()
            self.__timer_fps.tick(self.__configuracoes.max_fps)
