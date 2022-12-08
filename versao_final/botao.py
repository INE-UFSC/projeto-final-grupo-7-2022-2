from typing import Callable, Tuple

import pygame as pg

from configuracoes import Configuracoes


class Botao:
    def __init__(self, posicao: Tuple[int, int], imagens: Tuple[pg.Surface, pg.Surface], texto: str):
        self.__configuracoes = Configuracoes()
        self.__tela = pg.display.get_surface()
        self.__texto = self.__configuracoes.fonte_botao.render(texto, True, (255, 255, 255))
        self.__texto_rect = self.__texto.get_rect()

        self.__on_click_callback = None

        self.__posicao = posicao
        self.__imagens = imagens
        self.__rect = self.__imagens[0].get_rect(topleft=posicao)
        self.__ativo = 0

    def desenhar(self) -> None:
        self.__tela.blit(self.__imagens[self.__ativo], self.__posicao)
        if self.__ativo == 1:
            self.__texto_rect.center = (self.__rect.centerx + 2, self.__rect.centery + 2)
        else:
            self.__texto_rect.center = self.__rect.center
        self.__tela.blit(self.__texto, self.__texto_rect)

    def atualizar(self, evento: pg.event.Event) -> None:
        self.__ativo = 0
        if self.__rect.collidepoint(evento.pos):
            self.__ativo = 1
            if evento.type == pg.MOUSEBUTTONDOWN:
                if self.__on_click_callback:
                    self.__on_click_callback()

    def no_clique(self, callback: Callable) -> None:
        self.__on_click_callback = callback

    @property
    def imagens(self):
        return self.__imagens

    @imagens.setter
    def imagens(self, imagens):
        self.__imagens = imagens

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, ativo):
        self.__ativo = ativo

    @property
    def rect(self):
        return self.__rect

    @property
    def posicao(self):
        return self.__posicao

    @property
    def tela(self):
        return self.__tela

    @property
    def texto(self):
        return self.__texto

    @property
    def texto_rect(self):
        return self.__texto_rect
    
    @property
    def on_click_callback(self):
        return self.__on_click_callback