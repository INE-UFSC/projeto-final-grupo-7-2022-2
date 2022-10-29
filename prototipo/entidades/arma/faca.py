import pygame as pg
#from .arma import Arma

class Faca(pg.sprite.Sprite):
    def __init__(self):
        #super().__init__(groups)
        self.__escala = (14, 6)
        self.__image = pg.image.load("sprites/Faca.png").convert_alpha()
        self.__image = pg.transform.scale(self.__image, self.__escala)
        #self.__rect = self.__image.get_rect(center = player.recte.center)

    '''@property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")'''

    def usar_arma(self, screen, x, y, escala, sentido):
        print(sentido)
        if sentido == "Direita":
            screen.blit(self.__image, (x + int(escala*0.95),y + int(escala*0.75)))
        elif sentido == "Esquerda":
            imagem_esquerda = pg.transform.flip(self.__image, True, False)
            screen.blit(imagem_esquerda, (x - self.__escala[0] ,y + int(escala*0.75)))
        elif sentido == "Cima":
            imagem_cima = pg.transform.rotate(self.__image, 90)
            screen.blit(imagem_cima, (x + int(escala*0.95) ,(y - self.__escala[1])))
            print("Hmm")
        else:
            imagem_baixo = pg.transform.rotate(self.__image, 270)
            screen.blit(imagem_baixo, (x + int(escala*0.95),y + escala))