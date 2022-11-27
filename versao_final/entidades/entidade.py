from abc import ABC
import pygame as pg
from math import sin


class Entidade(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.velocidade = 0
        self.sprite = None
        self.direction = pg.math.Vector2()

        self.frame_index = 0
        self.animation_speed = 0.15

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

    @property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")

    def atualizar(self, delta: float):
        raise NotImplementedError("Atualizar não implementado")

    def desenhar(self):
        raise NotImplementedError("Desenhar não implementado")

    def receber_dano(self, dano: int):
        raise NotImplementedError("Receber dano não implementado")
