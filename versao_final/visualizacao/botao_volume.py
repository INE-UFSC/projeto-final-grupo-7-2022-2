from typing import Callable, Tuple

import pygame as pg

from .botao import Botao


class BotaoVolume(Botao):
    def __init__(self, posicao: Tuple[int, int], imagens: Tuple[pg.Surface, ...]):
        super().__init__(posicao, imagens, '')
        self.__volume = 0
        self.__tela = pg.display.get_surface()

    @property
    def volume(self) -> int:
        return self.__volume

    @volume.setter
    def volume(self, volume: int) -> None:
        self.__volume = volume

    def desenhar(self) -> None:
        if self.ativo == 1:
            self.imagens[self.__volume].set_alpha(255)
        else:
            self.imagens[self.__volume].set_alpha(200)
        self.__tela.blit(self.imagens[self.__volume], self.rect.topleft)