import pygame as pg
import os
from configuracoes import Configuracoes
from configuracoes import Singleton
import time


class Controlador_de_Musica(Singleton):
    def __init__(self) -> None:
        self.__configuracoes = Configuracoes()
        pg.mixer.init()
        self.__som_click = pg.mixer.Sound(self.__configuracoes.som_hit)
        self.__volume_musica = 0.5
        self.__volume_som = 1

    def iniciar_musica(self, path):
        pg.mixer.music.load(path)
        pg.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

    def parar_musica(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()

    def som_click(self):
        self.__som_click.play()

    #------------ método incompleto
    def tocar_som(self,som):
        self.som.play()

    def mudar_volume_musica(self):
        if self.__volume_musica == 1:
            self.__volume_musica = 0.75
        elif self.__volume_musica == 0.75:
            self.__volume_musica = 0.5
        elif self.__volume_musica == 0.5:
            self.__volume_musica = 0.25
        elif self.__volume_musica == 0.25:
            self.__volume_musica = 0
        else:
            self.__volume_musica = 1

        pg.mixer.music.set_volume(self.__volume_musica)

    def mudar_volume_som(self):
        if self.__volume_som == 1:
            self.__volume_som = 0.5
        elif self.__volume_som == 0.5:
            self.__volume_som = 0
        else:
            self.__volume_som = 1

        pg.mixer.Sound.set_volume(self.__volume_som)