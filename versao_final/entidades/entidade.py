import pygame as pg
from abc import ABC, abstractmethod
from math import sin
from configuracoes import Configuracoes


class Entidade(pg.sprite.Sprite, ABC):
    def __init__(self, fase, pos) -> None:
        super().__init__()
        self.__configuracoes = Configuracoes()
        self.__fase = fase
        self.__posicao = pos
        self.__obstacle_sprites = fase.colisores

        self.__status = None
        self.__velocidade = None
        self.__direction = pg.math.Vector2()
        self.__vida = None

        self.sprite = None
        self.frame_index = 0
        self.animation_speed = 0.15

    @property
    def configuracoes(self):
        return self.__configuracoes

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction):
        self.__direction = direction

    @property
    def fase(self):
        return self.__fase

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def posicao(self):
        return self.__posicao

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def velocidade(self):
        return self.__velocidade
    
    @velocidade.setter
    def velocidade(self, velocidade):
        self.__velocidade = velocidade

    @property
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, vida):
        self.__vida = vida

    def move(self, tempo_passado):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() * tempo_passado / 10

        # Realiza o movimento e checa a existência de colisões com a hitbox
        self.hitbox.x += self.direction.x * self.velocidade
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.velocidade
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    # Função usada para oscilar a visibilidade com base no seno
    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def registrar_na_fase(self, fase):
        raise NotImplementedError("Registrar na fase não implementado")

    def receber_dano(self, dano: int):
        self.__vida -= dano
        if self.__vida <= 0:
            self.__kill()

    def desenhar(self):
        return (self,)

    @abstractmethod
    def animate(self):
        pass

    @abstractmethod
    def atualizar(self, delta: float):
        pass

    @abstractmethod
    def obter_status(self, jogador):
        pass

    @abstractmethod
    def tipo(self):
        pass