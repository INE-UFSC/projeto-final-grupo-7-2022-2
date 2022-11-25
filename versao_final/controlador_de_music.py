import pygame as pg
import os
from configuracoes import Configuracoes
from configuracoes import Singleton


class Controlador_de_Musica(Singleton):
    def __init__(self) -> None:
        self.__configuracoes = Configuracoes()
        pg.mixer.init()
        self.__som_click = pg.mixer.Sound(self.__configuracoes.som_hit)

    def iniciar_musica(self, path):
        pg.mixer.music.load(path)
        pg.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

    def parar_musica(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()

    def som_click(self):
        self.__som_click.play()

    def tocar_com(self,som):
        self.som.play()