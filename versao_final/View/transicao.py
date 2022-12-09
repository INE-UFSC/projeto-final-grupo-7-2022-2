import pygame as pg
from configuracoes import Configuracoes


class Transicao:

    def __init__(self):
        self.__cfg = Configuracoes()

        self.__alfa = 0
        self.__mascara = pg.Surface((self.__cfg.largura_tela, self.__cfg.altura_tela))
        self.__mascara.fill((0, 0, 0))
        self.__mascara.set_alpha(self.__alfa)

        self.__iniciou = False
        self.__terminou = False

    def atualizar(self, tempo_passado):
        if not self.__iniciou:
            self.__iniciar(tempo_passado)
        if not self.__terminou:
            self.__terminar(tempo_passado)

    def __iniciar(self, tempo_passado):
        
        self.__alfa += tempo_passado // 2
        self.__mascara.set_alpha(self.__alfa)

        if self.__alfa >= 255:
            self.__alfa = 255
            self.__iniciou = True

    def __terminar(self, tempo_passado):
        
        self.__alfa -= tempo_passado // 2
        self.__mascara.set_alpha(self.__alfa)

        if self.__alfa <= 0:
            self.__alfa = 0
            self.__terminou = True

    def reiniciar(self):
        self.__terminou = False
        self.__iniciou = False
        self.__alfa = 0
        self.__mascara.set_alpha(self.__alfa)

    def desenhar(self):
        return self.__mascara

    @property
    def iniciou(self):
        return self.__iniciou
    
    @property
    def terminou(self):
        return self.__terminou
