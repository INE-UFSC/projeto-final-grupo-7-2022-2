import pygame as pg
from configuracoes import Configuracoes
from configuracoes import Singleton


class ControladorDeMusica(Singleton):
    def __init__(self) -> None:
        self.__configuracoes = Configuracoes()
        pg.mixer.init()
        self.__som_click = pg.mixer.Sound(self.__configuracoes.som_bandeira)
        self.__volume_musica = 0.5
        self.__volume_som = 0.5

    def volume_musica(self):
        if self.__volume_musica == 0.75:
            return 2
        elif self.__volume_musica == 0.5:
            return 1
        elif self.__volume_musica == 0.10:
            return 0
        else:
            return 3

    def volume_som(self):
        if self.__volume_som == 0.75:
            return 2
        elif self.__volume_som == 0.5:
            return 1
        elif self.__volume_som == 0.0:
            return 0
        else:
            return 3

    def iniciar_musica(self, path):
        pg.mixer.music.load(path)
        pg.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

    def parar_musica(self):
        pg.mixer.music.stop()
        pg.mixer.music.unload()

    def som_click(self):
        self.__som_click.play()

    # ------------ método incompleto
    #def tocar_som(self, som):
        #self.som.play()

    def mudar_volume_musica(self):
        if self.__volume_musica == 1.0:
            self.__volume_musica = 0.75
        elif self.__volume_musica == 0.75:
            self.__volume_musica = 0.5
        elif self.__volume_musica == 0.5:
            self.__volume_musica = 0.10
        elif self.__volume_musica == 0.10:
            self.__volume_musica = 0.0
        else:
            self.__volume_musica = 1.0

        pg.mixer.music.set_volume(self.__volume_musica)

    def mudar_volume_som(self):
        if self.__volume_som == 1.0:
            self.__volume_som = 0.75
        elif self.__volume_som == 0.75:
            self.__volume_som = 0.5
        elif self.__volume_som == 0.5:
            self.__volume_som = 0.10
        elif self.__volume_som == 0.10:
            self.__volume_som = 0.0
        else:
            self.__volume_som = 1.0

        pg.mixer.Sound.set_volume(self.__som_click, self.__volume_som)

    def seletor_de_musica(self, rotulo):

        path = None

        if rotulo == "menu_principal":
            path = self.__configuracoes.musica_menu
        elif rotulo == "menu_creditos":
            path = self.__configuracoes.musica_creditos
        elif rotulo == "menu_opcoes":
            path = self.__configuracoes.musica_opcoes
        elif rotulo == "menu_ranking":
            path = self.__configuracoes.musica_ranking
        elif rotulo == "menu_registro":
            path = self.__configuracoes.musica_registro
        elif rotulo == "fim_de_jogo":
            path = self.__configuracoes.musica_fim
        elif rotulo == "menu_pausa":
            path = self.__configuracoes.musica_creditos
        elif rotulo == "menu_vitoria":
            path = self.__configuracoes.musica_registro
        else:
            # Provisório
            path = self.__configuracoes.musica_menu

        self.parar_musica()
        self.iniciar_musica(path)
