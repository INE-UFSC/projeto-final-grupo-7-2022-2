import pygame as pg
from configuracoes import Configuracoes
#from .entidade import Entidade


class Jogador(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.__configuracoes = Configuracoes()

        self.__pos = pos
        self.__escala = 1.5 * self.__configuracoes.tamanhotile

        self.image = pg.transform.scale(pg.image.load('sprites/player.png').convert_alpha(), (self.__escala, self.__escala))
        self.rect = self.image.get_rect(topleft = pos)

        self.__obstacle_sprites = obstacle_sprites
        
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

    def move(self):
        if self.__direction.magnitude() != 0:
            self.__direction = self.__direction.normalize()
        # Realiza o movimento e checa a existência de colisões
        self.rect.x += self.__direction.x * self.__velocidade
        self.collision('horizontal')
        self.rect.y += self.__direction.y * self.__velocidade
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.__obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.__direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.__direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.__obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.__direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.__direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move()

    def renderizar(self, screen):
        screen.blit(self.image, self.__pos)
        
