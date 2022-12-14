import pygame


class CallbackDeEvento():
    def __init__(self, id: int, tipo_de_evento: int, callback: callable):
        self.__id = id
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
