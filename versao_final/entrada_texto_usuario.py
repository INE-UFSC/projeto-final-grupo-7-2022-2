import pygame as pg
from configuracoes import Configuracoes
import time


class EntradaTextoUsuario:
    def __init__(self, pos, largura, altura, tela):
        pg.init()
        self.__configuracoes = Configuracoes()

        self.__pos = pos
        self.__largura = largura
        self.__altura = altura
        self.__tela = tela
        self.__retangulo = pg.Rect(self.__pos[0], self.__pos[1], self.__largura, self.__altura)

        self.__texto_usuario = ''
        self.__fonte_render = self.__configuracoes.fonte_digitar.render(self.__texto_usuario, True, (255, 255, 255))
        self.__fonte_ret = self.__fonte_render.get_rect()
        self.__fonte_ret.topleft = pos
        self.__cursor = pg.Rect(self.__fonte_ret.bottomright, (3, self.__fonte_ret.height - 8))

        self.__ativo = False
        self.__cor_ativa = pg.Color(33, 38, 43)
        self.__cor_passiva = pg.Color(99, 118, 137)
        self.__cor_atual = self.__cor_passiva

    @property
    def texto_usuario(self):
        return self.__texto_usuario

    @texto_usuario.setter
    def texto_usuario(self, texto_usuario):
        self.__texto_usuario = texto_usuario

    def atualizar(self, eventos: list):
        for evento in eventos:         
            if evento.type == pg.KEYDOWN and self.__ativo:
                if evento.key == pg.K_BACKSPACE:
                    self.__texto_usuario = self.__texto_usuario[:-1]
                elif evento.key == pg.K_RETURN or evento.key == pg.K_KP_ENTER or evento.key == pg.K_TAB:
                    self.__ativo = False
                elif pg.font.Font.size(self.__configuracoes.fonte_digitar, self.__texto_usuario + evento.unicode)[0] < self.__largura - 5:
                    self.__texto_usuario += evento.unicode

        pos = pg.mouse.get_pos()
        if self.__retangulo.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.__ativo:
                self.__ativo = True
        elif pg.mouse.get_pressed()[0] == 1 and self.__ativo:
            self.__ativo = False
        self.__fonte_render = self.__configuracoes.fonte_digitar.render(self.__texto_usuario, True, (255, 255, 255))

    def desenhar(self, superficie):
        if self.__ativo:
            self.__cor_atual = self.__cor_ativa
            self.__fonte_ret.size = self.__fonte_render.get_size()
            self.__cursor.bottomleft = self.__fonte_ret.bottomright
        else:
            self.__cor_atual = self.__cor_passiva
        
        pg.draw.rect(self.__tela, self.__cor_atual, self.__retangulo)
        pg.draw.rect(self.__tela, (255, 255, 255), self.__retangulo, 2, 5)
        if time.time() % 1 > 0.5 and self.__ativo:
            pg.draw.rect(self.__tela, (255, 255, 255), self.__cursor)

        superficie.blit(self.__fonte_render, self.__pos)