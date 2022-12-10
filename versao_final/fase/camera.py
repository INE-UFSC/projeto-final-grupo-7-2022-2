from typing import List

import pygame as pg

from visualizacao import SuperficiePosicionada

from .gerenciador_de_grupos import GerenciadorDeGrupos


class Camera():
    def __init__(self, gerenciador_de_grupos: GerenciadorDeGrupos):
        self.__tela = pg.display.get_surface()
        self.__quadro = pg.surface.Surface(self.__tela.get_size())

        self.__gerenciador_de_grupos = gerenciador_de_grupos

        centro_da_tela_x = self.__tela.get_width() // 2
        centro_da_tela_y = self.__tela.get_height() // 2

        self.__centro_da_tela = pg.Vector2(centro_da_tela_x, centro_da_tela_y)

    def __desenhar_camada_inferior(self, deslocamento: pg.Vector2):
        chao = self.__gerenciador_de_grupos.chao
        posicao = chao.posicao - deslocamento
        self.__quadro.blit(chao.superficie, posicao)

    def __desenhar_camada_superior(self, deslocamento: pg.Vector2):
        blocos_superiores = self.__gerenciador_de_grupos.blocos_superiores
        posicao = blocos_superiores.posicao - deslocamento
        self.__quadro.blit(blocos_superiores.superficie, posicao)

    def __desenhar_lista_pelo_y(self, deslocamento: pg.Vector2, lista: List[SuperficiePosicionada]):
        lista.sort(key=lambda superficie: superficie.rect.centery)
        for superficie_posicionada in lista:
            posicao = superficie_posicionada.posicao - deslocamento
            self.__quadro.blit(superficie_posicionada.superficie, posicao)

    def desenhar(self, centro_do_desenho: pg.Vector2, superficie_posicionadas: List[SuperficiePosicionada]) -> pg.Surface:
        self.__quadro.fill('black')
        # o deslocamento que a posição dos sprites visíveis deve ter para simular uma câmera
        deslocamento = centro_do_desenho - self.__centro_da_tela

        self.__desenhar_camada_inferior(deslocamento)
        # Ao invés de desenharmos os objetos numa posição fixa, nos os posicionamos de acordo com o centro.
        # Além disso, a ordem de desenho dos objetos na tela é crescente com relação a sua posição y
        lista_de_superficies_posicionadas = self.__gerenciador_de_grupos.blocos_estaticos.copy()
        lista_de_superficies_posicionadas.extend(self.__gerenciador_de_grupos.blocos_dinamicos)
        lista_de_superficies_posicionadas.extend(superficie_posicionadas)
        self.__desenhar_lista_pelo_y(deslocamento, lista_de_superficies_posicionadas)
        

        self.__desenhar_camada_superior(deslocamento)

        return self.__quadro
