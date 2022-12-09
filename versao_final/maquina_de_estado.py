from typing import List
import pygame as pg
from controlador_de_musica import ControladorDeMusica

from estados import Estado


class MaquinaDeEstado:
    def __init__(self):
        self.__estados = {}
        self.__estado_pilha: List[str] = []
        self.__estado_atual_rotulo: str | None = None
        self.__estado_inicial_rotulo: str | None = None
        self.__controlador_de_musica = ControladorDeMusica()

    @property
    def estado_inicial(self) -> Estado:
        return self.__estados[self.__estado_inicial_rotulo]

    def definir_estado_inicial(self, estado_inicial_rotulo: str):
        self.__estado_inicial_rotulo = estado_inicial_rotulo

    @property
    def estado_atual(self) -> Estado:
        return self.__estados[self.__estado_atual_rotulo]

    def adicionar_estado(self, rotulo: str, estado: Estado) -> None:
        self.__estados[rotulo] = estado
        if len(self.__estados) == 1 and self.__estado_inicial_rotulo is None:
            self.__estado_inicial_rotulo = rotulo
        if self.__estado_atual_rotulo is None:
            self.__estado_atual_rotulo = rotulo

    def mover_para_estado(self, rotulo: str) -> None:
        if (rotulo != self.__estado_atual_rotulo):
            self.__estado_pilha.append(self.__estado_atual_rotulo)
            self.__estado_atual_rotulo = rotulo
            self.estado_atual.iniciar()
            self.__controlador_de_musica.parar_musica()
            self.__controlador_de_musica.seletor_de_musica(rotulo)

    def voltar_para_inicio(self) -> None:
        self.__estado_atual_rotulo = self.__estado_inicial_rotulo
        self.__controlador_de_musica.seletor_de_musica(self.__estado_inicial_rotulo)
        print(self.__estado_inicial_rotulo)
        self.__controlador_de_musica.parar_musica()
        self.__estado_pilha = []
        self.estado_atual.iniciar()

    def voltar(self) -> None:
        ultimo_estado_rotulo = self.__estado_pilha.pop()
        if ultimo_estado_rotulo is not None:
            self.__estado_atual_rotulo = ultimo_estado_rotulo
            self.__controlador_de_musica.seletor_de_musica(self.__estado_atual_rotulo)
        else:
            self.__controlador_de_musica.parar_musica()
            self.voltar_para_inicio()


    def iniciar(self) -> None:
        self.estado_atual.iniciar()
        self.__controlador_de_musica.seletor_de_musica(self.__estado_inicial_rotulo)
