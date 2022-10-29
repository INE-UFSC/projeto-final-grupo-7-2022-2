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

        # Posições:
        self.__x_atual = x 
        self.__y_atual = y
        self.__x_inicial = x
        self.__y_inicial = y


    def atirar(self, sentido, superficie, escala):
        #self.__balas.append(self.__image)

        if sentido == "Direita":
            if self.__x_atual <= self.__x_inicial + self.__raio:
                superficie.blit(self.__image, (self.__x_atual + int(escala*0.95),self.__y_inicial+ int(escala*0.75)))
                self.__x_atual += self.__velocidade
            
        elif sentido == "Esquerda":
            imagem_esquerda = pg.transform.flip(self.__image, True, False)
            if self.__x_atual >= self.__x_inicial - self.__raio:
                superficie.blit(imagem_esquerda, (self.__x_atual - self.__escala[0] ,self.__y_inicial+ int(escala*0.75)))
                self.__x_atual -= self.__velocidade
            
        elif sentido == "Cima":
            imagem_cima = pg.transform.rotate(self.__image, 90)
            if self.__y_atual >=self.__y_inicial - self.__raio:
                superficie.blit(imagem_cima, (self.__x_atual + int(escala*0.95) ,(self.__y_inicial- self.__escala[1])))
                self.__y_atual -= self.__velocidade
            
        else:
            imagem_baixo = pg.transform.rotate(self.__image, 270)
            if self.__y_atual <= self.__y_inicial + self.__raio:
                superficie.blit(imagem_baixo, (self.__x_atual + int(escala*0.95),self.__y_inicial+ escala))
                self.__y_atual += self.__velocidade

    @property
    def ativo(self):
        return self.__raio >= abs(self.__x_atual - self.__x_inicial) or self.__raio >= abs(self.__y_atual - self.__y_inicial)
