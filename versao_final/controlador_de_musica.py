import pygame as pg
from configuracoes import Configuracoes
from configuracoes import Singleton


class ControladorDeMusica(Singleton):
    def __init__(self) -> None:
        self.__configuracoes = Configuracoes()
        pg.mixer.init()
        self.__som_click = [pg.mixer.Sound(self.__configuracoes.som_bandeira), 
                            pg.mixer.Sound(self.__configuracoes.som_folha), 
                            pg.mixer.Sound(self.__configuracoes.som_tijolo),
                            pg.mixer.Sound(self.__configuracoes.som_tiro),
                            pg.mixer.Sound(self.__configuracoes.som_flecha),
                            pg.mixer.Sound(self.__configuracoes.som_faca)]
        self.__volume_musica = [0.0, 0.1, 0.5, 1.0]
        self.__volume_som = [0.0, 0.1, 0.5, 1.0]

        self.__indice_volume_musica = 1
        self.__indice_volume_som = 1

        pg.mixer.music.set_volume(self.__volume_musica[self.__indice_volume_musica])
        for i in self.__som_click:
            pg.mixer.Sound.set_volume(i, self.__volume_som[self.__indice_volume_som])

    @property
    def volume_musica(self):
        return self.__indice_volume_musica

    @property
    def volume_som(self):
        return self.__indice_volume_som

    def iniciar_musica(self, path):
        pg.mixer.music.load(path)
        pg.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

    def parar_musica(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()

    def som_botao(self, tipo:str):
        if tipo == "bandeira":
            self.__som_click[0].play()
        elif tipo == "folha":
            self.__som_click[1].play()
        elif tipo == "nuvem":
            self.__som_click[0].play()
        elif tipo == "tijolo":
            self.__som_click[2].play()
        
    def som_ataque(self, tipo:str):
        if tipo == "pistola":
            self.__som_click[3].play()
        elif tipo == "flecha":
            self.__som_click[4].play()
        elif tipo == "faca":
            self.__som_click[5].play()

    def mudar_volume_musica(self):
        self.__indice_volume_musica = (self.__indice_volume_musica + 1) % len(self.__volume_musica)
        pg.mixer.music.set_volume(self.__volume_musica[self.__indice_volume_musica])

    def mudar_volume_som(self):
        for i in self.__som_click:
            self.__indice_volume_som = (self.__indice_volume_som + 1) % len(self.__volume_som)
            pg.mixer.Sound.set_volume(i, self.__volume_som[self.__indice_volume_som])