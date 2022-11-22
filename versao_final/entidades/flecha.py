import pygame as pg


class Flecha(pg.sprite.Sprite):
    def __init__(self, fase, groups, pos_inicial, direcao, dano_no_jogador) -> None:
        super().__init__(groups)

        self.tipo_sprite = 'flecha'
        self.__fase = fase

        # Imagem
        self.__escala = (8, 8)
        self.__image = pg.Surface(self.__escala)
        self.__image.fill((255, 255, 255))
        self.__rect = self.__image.get_rect(center = pos_inicial)

        # Movimento
        self.__direcao = direcao
        self.__velocidade = 15

        # Dano
        self.__alvo = self.__fase.jogador
        self.__parede = self.__fase.grupo_de_obstaculos
        self.__dano = 1
        self.__dano_no_jogador = dano_no_jogador

        # Ativo
        self.__ativo = True

    def tipo(self):
        return 'flecha'

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
        if self.__alvo.hitbox.colliderect(self.__rect):
            self.kill()
            self.__ativo = False
            self.__dano_no_jogador()
        
        for parede in self.__parede:
            if parede.hitbox.colliderect(self.__rect):
                self.__ativo = False
                self.kill()


    def desenhar(self):
        return (self,)

    def atualizar(self, tempo):
        self.move()
        self.colisao()