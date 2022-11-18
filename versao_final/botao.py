import pygame as pg

class Botao:
    def __init__(self, pos, largura, altura):
        self.__imagens = None
        self.__on_click_callback = None
        self.__status = 'nao_clicado'
        self.__pos = pos
        self.__largura = largura
        self.__altura = altura
        

        self.__cor = (255, 0, 0)
        self.__image = pg.Surface((self.__largura, self.__altura))
        self.__image.fill(self.__cor)

        self.__rect = self.__image.get_rect(topleft=pos)
        self.__on_click_callback = None
        
    def desenhar(self):
        return self.__image

    def atualizar(self):
        pos = pg.mouse.get_pos()

        if self.__rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                if self.__on_click_callback:
                    self.__on_click_callback()

    def on_click(self, callback):
        self.__on_click_callback = callback