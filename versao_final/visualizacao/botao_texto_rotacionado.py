from typing import Callable, Tuple

import pygame as pg

from .botao import Botao


class BotaoTextoRotacionado(Botao):
    def __init__(self, posicao: Tuple[int, int], imagens: Tuple[pg.Surface, pg.Surface], texto: str):
        super().__init__(posicao, imagens, texto)

    def desenhar(self) -> None:
        self.tela.blit(self.imagens[self.ativo], self.posicao)
        if self.ativo == 1:
            texto_desenho = pg.transform.rotate(self.texto, -2)
            self.texto_rect.midleft = (self.rect.midleft[0] + 32, self.rect.midleft[1] - 8)
            self.tela.blit(texto_desenho, self.texto_rect)
        else:
            self.texto_rect.midleft = (self.rect.midleft[0] + 30, self.rect.midleft[1] - 5)
            self.tela.blit(self.texto, self.texto_rect)