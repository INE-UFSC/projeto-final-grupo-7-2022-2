import time
from typing import List

import pygame as pg

from configuracoes import Configuracoes


class EntradaTextoUsuario:
    def __init__(self, posicao: pg.Vector2, largura: int, altura: int):
        pg.init()
        self.__configuracoes = Configuracoes()

        self.__tela = pg.display.get_surface()
        self.__rect = pg.Rect(posicao.x, posicao.y, largura, altura)

        self.__texto_usuario = ''
        self.__fonte_render = self.__configuracoes.fonte_digitar.render(self.__texto_usuario, True, (255, 255, 255))
        self.__fonte_rect = self.__fonte_render.get_rect()
        self.__fonte_rect.topleft = self.__rect.topleft
        self.__cursor = pg.Rect(self.__rect.bottomright, (3, self.__fonte_rect.height - 8))

        self.__ativo = False
        self.__cor_ativa = pg.Color(24, 27, 31)
        self.__cor_passiva = pg.Color(33, 38, 43)
        self.__cor_atual = self.__cor_passiva

    @property
    def texto_usuario(self) -> str:
        return self.__texto_usuario

    @texto_usuario.setter
    def texto_usuario(self, texto_usuario: str):
        self.__texto_usuario = texto_usuario

    def atualizar(self, eventos: List[pg.event.Event]):
        for evento in eventos:
            if evento.type == pg.KEYDOWN and self.__ativo:
                if evento.key == pg.K_BACKSPACE:
                    self.__texto_usuario = self.__texto_usuario[:-1]
                elif evento.key == pg.K_RETURN or evento.key == pg.K_KP_ENTER or evento.key == pg.K_TAB:
                    self.__ativo = False
                elif pg.font.Font.size(self.__configuracoes.fonte_digitar, self.__texto_usuario + evento.unicode)[0] < self.__rect.width - 5:
                    self.__texto_usuario += evento.unicode

        posicao = pg.mouse.get_pos()
        if self.__rect.collidepoint(posicao):
            if pg.mouse.get_pressed()[0] == 1 and not self.__ativo:
                self.__ativo = True
        elif pg.mouse.get_pressed()[0] == 1 and self.__ativo:
            self.__ativo = False
        self.__fonte_render = self.__configuracoes.fonte_digitar.render(self.__texto_usuario, True, (255, 255, 255))

    def desenhar(self) -> None:
        if self.__ativo:
            self.__cor_atual = self.__cor_ativa
            self.__fonte_rect.size = self.__fonte_render.get_size()
            self.__cursor.bottomleft = self.__fonte_rect.bottomright
        else:
            self.__cor_atual = self.__cor_passiva

        pg.draw.rect(self.__tela, self.__cor_atual, self.__rect, border_radius=5)
        if time.time() % 1 > 0.5 and self.__ativo:
            pg.draw.rect(self.__tela, (255, 255, 255), self.__cursor)

        self.__tela.blit(self.__fonte_render, self.__rect.topleft)
