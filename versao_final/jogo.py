import sys
import pygame as pg
import pygame.time as pg_time
from maquina_de_estado import MaquinaDeEstado
from configuracoes import Configuracoes
from evento_tps import evento_TPS


class Jogo:
    def __init__(self):
        pg.init()
       # pg.mixer.init()

        self.__maquina_de_estado = MaquinaDeEstado()
        self.__configuracoes = Configuracoes()

        self.__tela = pg.display.set_mode((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        pg.display.set_caption('SUPER LAMPARINA ARFANTE')


        self.__timer_fps = pg.time.Clock()
        self.__timer_tps = pg.time.Clock()
        pg_time.set_timer(evento_TPS, 1000 // self.__configuracoes.tps)

    @property
    def tela(self):
        return self.__tela

    @property
    def maquina_de_estado(self):
        return self.__maquina_de_estado

    def iniciar(self):
        self.maquina_de_estado.mover_para_estado("menu_principal")
        eventos = []
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == evento_TPS.type:
                    self.maquina_de_estado.estado_atual.atualizar(eventos, self.__timer_tps.tick())
                    eventos = []
                else:
                    eventos.append(event)

            self.maquina_de_estado.estado_atual.desenhar()
            #self.maquina_de_estado.estado_atual.tocar_musica()
            pg.display.update()
            self.__timer_fps.tick(self.__configuracoes.max_fps)
