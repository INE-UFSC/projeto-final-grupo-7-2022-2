import pygame as pg
from configuracoes import Configuracoes


class Botao:
    def __init__(self, pos, imagens, texto):
        self.__configuracoes = Configuracoes()
        self.__texto = self.__configuracoes.fonte_botao.render(texto, True, (255, 255, 255))
        self.__texto_rect = self.__texto.get_rect()

        self.__on_click_callback = None

        self.__pos = pos
        self.__imagens = imagens
        self.__rect = self.__imagens[0].get_rect(topleft=pos)
        self.__ativo = 0
        
    def desenhar(self, superficie):
        superficie.blit(self.__imagens[self.__ativo], self.__pos)
        if self.__ativo == 1:
            texto_desenho = pg.transform.rotate(self.__texto, -3)
            self.__texto_rect.center = (self.__rect.centerx - 40, self.__rect.centery - 10)
            superficie.blit(texto_desenho, self.__texto_rect)
        else:
            self.__texto_rect.center = (self.__rect.centerx - 40, self.__rect.centery)
            superficie.blit(self.__texto, self.__texto_rect)

    def atualizar(self):
        pos = pg.mouse.get_pos()
        self.__ativo = 0

        if self.__rect.collidepoint(pos):
            self.__ativo = 1
            if pg.mouse.get_pressed()[0] == 1:
                if self.__on_click_callback:
                    self.__on_click_callback()

    def on_click(self, callback):
        self.__on_click_callback = callback