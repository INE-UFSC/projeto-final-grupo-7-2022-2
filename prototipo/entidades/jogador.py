import pygame as pg
#from .entidade import Entidade


class Jogador(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y
        self.__velocidade = 2
        self.__dimension_x = 50
        self.__dimension_y = 70
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
        pg.draw.rect(screen,(255, 0, 0), (self.__x, self.__y, self.__dimension_x, self.__dimension_y))
