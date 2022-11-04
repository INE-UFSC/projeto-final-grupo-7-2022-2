from re import X
import pygame as pg


class Bala(pg.sprite.Sprite):
    def __init__(self, fase, groups, pos_inicial, direcao) -> None:
        super().__init__(groups)

        self.tipo_sprite = 'bala'
        self.__fase = fase

        # Imagem
        self.__escala = (4, 4)
        self.__image = pg.Surface(self.__escala)
        self.__image.fill((255, 255, 255))
        self.__rect = self.__image.get_rect(center = pos_inicial)

        # Movimento
        self.__direcao = direcao
        self.__velocidade = 10

        # Dano
        self.__alvos = self.__fase.attackable_sprites
        self.__parede = self.__fase.grupo_de_obstaculos
        self.__dano = 1

        # Ativo
        self.__ativo = True

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, ativo):
        self.__ativo = ativo

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    def move(self):
        # Transforma o comprimento do vetor em 1
        self.__direcao = self.__direcao.normalize()

        # Move a bala baseado na direção e velocidade
        self.__rect.x += self.__direcao.x * self.__velocidade
        self.__rect.y += self.__direcao.y * self.__velocidade

    def colisao(self):
        for alvo in self.__alvos:
            if alvo.hitbox.colliderect(self.__rect):
                self.kill()
                self.__ativo = False
                alvo.toma_dano()
        
        for parede in self.__parede:
            if parede.hitbox.colliderect(self.__rect):
                self.kill()
                self.__ativo = False

    @property
    def ativo(self):
        return self.__ativo


    def desenhar(self):
        return (self,)

    def atualizar(self, tempo):
        self.move()
        self.colisao()