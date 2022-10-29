from re import X
import pygame as pg

class Bala(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        #super().__init__(groups)
        self.__escala = (14, 6)
        self.__image = pg.image.load("sprites/Faca.png").convert_alpha()
        self.__image = pg.transform.scale(self.__image, self.__escala)
        self.__raio = 100
        self.__balas_max = 6
        self.__velocidade = 7
        self.__x = x
        self.__y = y


    def atirar(self, sentido, superficie,x, y, escala):
        #self.__balas.append(self.__image)

        if sentido == "Direita":
            if self.__x <= x + self.__raio:
                superficie.blit(self.__image, (self.__x + int(escala*0.95),y + int(escala*0.75)))
                self.__x += self.__velocidade
            
        elif sentido == "Esquerda":
            imagem_esquerda = pg.transform.flip(self.__image, True, False)
            if self.__x >= x - self.__raio:
                superficie.blit(imagem_esquerda, (self.__x - self.__escala[0] ,y + int(escala*0.75)))
                self.__x -= self.__velocidade
            
        elif sentido == "Cima":
            imagem_cima = pg.transform.rotate(self.__image, 90)
            if self.__y >= y - self.__raio:
                superficie.blit(imagem_cima, (self.__x + int(escala*0.95) ,(y - self.__escala[1])))
                self.__y -= self.__velocidade
            
        else:
            imagem_baixo = pg.transform.rotate(self.__image, 270)
            if self.__y <= y + self.__raio:
                superficie.blit(imagem_baixo, (self.__x + int(escala*0.95),y + escala))
                self.__y += self.__velocidade

    def ativa(self,x, y):
        return self.__raio >= abs(self.__x - x) or self.__raio >= abs(self.__y - y)
