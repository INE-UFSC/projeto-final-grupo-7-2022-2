from typing import Callable

import pygame


class CallbackDeEvento():
    def __init__(self, identificador: int, tipo_de_evento: int, callback: Callable):
        self.__id = identificador
        self.__tipo_de_evento = tipo_de_evento
        self.__callback = callback

    @property
    def id(self):
        return self.__id

    @property
    def tipo(self):
        return self.__tipo_de_evento

    def disparar(self, evento: pygame.event.Event):
        self.__callback(evento)
