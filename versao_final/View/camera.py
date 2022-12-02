from typing import List

import pygame as pg

from superficie_posicionada import SuperficiePosicionada


class Camera():
    def __init__(self):
        self.__tela = pg.display.get_surface()

        centro_da_tela_x = self.__tela.get_width() // 2
        centro_da_tela_y = self.__tela.get_height() // 2

        self.__centro_da_tela = pg.Vector2(centro_da_tela_x, centro_da_tela_y)

    @property
    def chao(self) -> pg.Surface:
        return self.__chao

    @chao.setter
    def chao(self, chao: pg.Surface):
        self.__chao = chao

    @property
    def blocos(self) -> List[SuperficiePosicionada]:
        return self.__blocos

    @blocos.setter
    def blocos(self, blocos: List[SuperficiePosicionada]):
        self.__blocos = blocos

    @property
    def estruturas(self) -> List[SuperficiePosicionada]:
        return self.__estruturas

    @estruturas.setter
    def estruturas(self, estruturas: List[SuperficiePosicionada]):
        self.__estruturas = estruturas

    def __desenhar_lista_pelo_y(self, deslocamento: pg.Vector2, lista: List[SuperficiePosicionada]):
        lista.sort(key=lambda superficie: superficie.rect.centery)
        for superficie_posicionada in lista:
            posicao = superficie_posicionada.posicao - deslocamento
            self.__tela.blit(superficie_posicionada.superficie, posicao)

    def desenhar(self, centro_do_desenho: pg.Vector2, superficie_posicionadas: List[SuperficiePosicionada]):
        # o deslocamento que a posição dos sprites visíveis deve ter para simular uma câmera
        deslocamento = centro_do_desenho - self.__centro_da_tela

        self.__tela.blit(self.__chao, -deslocamento)

        # Ao invés de desenharmos os objetos numa posição fixa, nos os posicionamos de acordo com o centro.
        # Além disso, a ordem de desenho dos objetos na tela é crescente com relação a sua posição y
        self.__desenhar_lista_pelo_y(deslocamento, self.__estruturas)
        lista_de_superficies_posicionadas = self.__blocos.copy()
        lista_de_superficies_posicionadas.extend(superficie_posicionadas)
        self.__desenhar_lista_pelo_y(deslocamento, lista_de_superficies_posicionadas)
