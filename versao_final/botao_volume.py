import pygame as pg
from botao import Botao
from typing import Callable, Tuple


class BotaoVolume(Botao):
    def __init__(self, posicao: Tuple[int, int], imagens: Tuple[pg.Surface, pg.Surface], texto: str):
        super().__init__(posicao, imagens, texto)

    def atualizar(self, evento: pg.event.Event, imagens) -> None:
        self.ativo = 0
        if self.rect.collidepoint(evento.pos):
            self.ativo = 1
            if evento.type == pg.MOUSEBUTTONDOWN:
                if self.on_click_callback:
                    self.on_click_callback()
                    self.imagens = imagens
