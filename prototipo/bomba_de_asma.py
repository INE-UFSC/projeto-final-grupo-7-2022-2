import pygame as pg


class BombaDeAsma(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.tipo_sprite = 'bomba_asma'

    def atualizar(self, eventos: list):
        raise NotImplementedError("Atualizar não implementado")

    def renderizar(self):
        raise NotImplementedError("Renderizar não implementado")
