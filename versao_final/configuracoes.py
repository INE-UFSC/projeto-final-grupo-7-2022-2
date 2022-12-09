import pygame as pg
from singleton import Singleton
import os


class Configuracoes(Singleton):
    def __init__(self):
        self.__largura_tela = 1280
        self.__altura_tela = 720
        self.__tamanho_botoes = (180, 130)

        self.__volume_musica = None

        self.__tamanho_tile = 64
        self.__max_fps = 240
        self.__tps = 60

        self.__musica_menu = os.path.join('recursos', 'musicas', 'principal.mp3')
        self.__musica_creditos = os.path.join('recursos', 'musicas', 'creditos.mp3')
        self.__musica_fim = os.path.join('recursos', 'musicas', 'fim_de_jogo.mp3')
        self.__musica_ranking = os.path.join('recursos', 'musicas', 'ranking.mp3')
        self.__musica_registro = os.path.join('recursos', 'musicas', 'registro.mp3')
        self.__musica_opcoes = os.path.join('recursos', 'musicas', 'som_grama.ogg')
        self.__musica_jogo = os.path.join('recursos', 'musicas', 'jogo.mp3')

        self.__som_bandeira = os.path.join('recursos', 'musicas', 'som_bandeira.ogg')

        pg.font.init()
        self.__fonte_titulo = pg.font.Font(os.path.join('recursos', 'fontes', 'FieldGuide.ttf'), 100)
        self.__fonte_botao = pg.font.Font(os.path.join('recursos', 'fontes', 'FieldGuide.ttf'), 55)
        self.__fonte_digitar = pg.font.Font(os.path.join('recursos', 'fontes', 'FieldGuide.ttf'), 82)

        self.__fases = ['test2']

    @property
    def fases(self):
        return self.__fases

    @property
    def fonte_titulo(self):
        return self.__fonte_titulo

    @property
    def fonte_botao(self):
        return self.__fonte_botao

    @property
    def fonte_digitar(self):
        return self.__fonte_digitar

    @property
    def tps(self):
        return self.__tps

    @property
    def max_fps(self):
        return self.__max_fps

    @property
    def tamanho_tile(self):
        return self.__tamanho_tile

    @property
    def largura_tela(self):
        return self.__largura_tela

    @property
    def altura_tela(self):
        return self.__altura_tela

    @property
    def volume_musica(self):
        return self.__volume_musica

    @volume_musica.setter
    def volume_musica(self, volume_musica):
        self.__volume_musica = volume_musica

    @property
    def musica_menu(self):
        return self.__musica_menu

    @property
    def musica_creditos(self):
        return self.__musica_creditos

    @property
    def som_bandeira(self):
        return self.__som_bandeira

    @property
    def musica_opcoes(self):
        return self.__musica_opcoes

    @property
    def musica_fim(self):
        return self.__musica_fim

    @property
    def musica_ranking(self):
        return self.__musica_ranking

    @property
    def musica_registro(self):
        return self.__musica_registro

    @property
    def musica_jogo(self):
        return self.__musica_jogo

    @property
    def tamanho_botoes(self):
        return self.__tamanho_botoes