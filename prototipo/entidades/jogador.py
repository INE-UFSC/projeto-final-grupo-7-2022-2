import pygame as pg
#from .entidade import Entidade


class Jogador(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        self.__escala = 64
        self.__x = x
        self.__y = y
        self.__image = pg.image.load('sprites/player.png').convert_alpha()
        self.__rect = self.__image.get_rect(topleft = (self.__x, self.__y))
        self.__image = pg.transform.scale(self.__image, (self.__escala, self.__escala))
        self.__velocidade = 2
        self.__direction = pg.math.Vector2()
    
    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.__direction.y = -1
        elif keys[pg.K_DOWN]:
            self.__direction.y = 1
        else:
            self.__direction.y = 0

        if keys[pg.K_RIGHT]:
            self.__direction.x = 1
        elif keys[pg.K_LEFT]:
            self.__direction.x = -1
        else:
            self.__direction.x = 0

    def mover(self):
        if self.__direction.magnitude() != 0:
            self.__direction = self.__direction.normalize()

        self.__x += self.__direction.x * self.__velocidade
        self.__y += self.__direction.y * self.__velocidade
        

    def atualizar(self):
        self.input()
        self.mover()

    def renderizar(self, screen):
        screen.blit(self.__image, (self.__x,self.__y))
