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
            texto_desenho = pg.transform.rotate(self.__texto, -2)
            self.__texto_rect.midleft = (self.__rect.midleft[0] + 32, self.__rect.midleft[1] - 8)
            self.__tela.blit(texto_desenho, self.__texto_rect)
        else:
            self.__texto_rect.midleft = (self.__rect.midleft[0] + 30, self.__rect.midleft[1] - 5)
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
