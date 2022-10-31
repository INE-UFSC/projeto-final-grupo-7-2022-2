import pygame as pg
from configuracoes import Configuracoes
from entidades.arma.faca import Faca
from entidades.arma.pistola import Pistola
from spritesheet import Spritesheet
#from .entidade import Entidade


class Jogador(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, screen) -> None:
        super().__init__(groups)
        self.__configuracoes = Configuracoes()

        self.__pos = pos
        self.__escala = 1.5 * self.__configuracoes.tamanhotile

        # Imagem e hitbox
        self.__spritesheet = Spritesheet("skelet", 1)
        self.image = self.image('idle_0.png')
        self.animations = self.__spritesheet.animation_frames
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -8)

        self.__obstacle_sprites = obstacle_sprites
        
        # Movimento
        self.__velocidade = 5
        self.__direction = pg.math.Vector2()
        self.__attacking = False
        self.__attack_cd = 400
        self.__attack_time = None

        # Animação
        self.__status = 'right'
        self.__frame_index = 0
        self.__animation_speed = 0.15

        # Armas
        self.__faca = Faca()
        self.__pistola = Pistola()

        self.__janela = screen
    
    def image(self, sprite: str):
        return self.__spritesheet.get_sprite(sprite)

    def input(self):
        keys = pg.key.get_pressed()

        # Entradas de movimentação:
        if keys[pg.K_UP]:
            self.__direction.y = -1

        elif keys[pg.K_DOWN]:
            self.__direction.y = 1

        else:
            self.__direction.y = 0

        if keys[pg.K_RIGHT]:
            self.__direction.x = 1
            self.__status = "right"
        elif keys[pg.K_LEFT]:
            self.__direction.x = -1
            self.__status = "left"
        else:
            self.__direction.x = 0

        # Entradas de ataque:
        if keys[pg.K_SPACE] and not self.__attacking:
            self.__attacking = True
            self.__attack_time = pg.time.get_ticks()
            self.__pistola.usar_arma(self.__janela, self.rect.x, self.rect.y, self.__escala, self.__status)

    def status(self):
        if self.__direction.x == 0 and self.__direction.y == 0:
            if not 'idle' in self.__status and not 'attack' in self.__status:
                self.__status += '_idle'
        else:
            if 'idle' in self.__status:
                self.__status = self.__status.replace('_idle','')
            
        
        # if self.__direction.y > 0:
        #     if not 'down' in self.__status:
        #         self.__status += '_down'
        # elif self.__direction.y < 0:
        #     if not 'up' in self.__status:
        #         self.__status += '_up'
        # else:
        #     if 'up' in self.__status:
        #         self.__status.replace('_up','')
        #     elif 'down' in self.__status:
        #         self.__status.replace('_down','')


        if self.__attacking:
            self.__direction.x = 0
            self.__direction.y = 0
            if not 'attack' in self.__status:
                if 'idle' in self.__status:
                    self.__status = self.__status.replace('_idle','_attack')
                else:
                    self.__status += '_attack'
        else:
            if 'attack' in self.__status:
                self.__status = self.__status.replace('_attack', '')

    def move(self):
        if self.__direction.magnitude() != 0:
            self.__direction = self.__direction.normalize()

        # Realiza o movimento e checa a existência de colisões com a hitbox
        self.hitbox.x += self.__direction.x * self.__velocidade
        self.collision('horizontal')
        self.hitbox.y += self.__direction.y * self.__velocidade
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.__obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.__direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.__direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.__obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.__direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.__direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        tempo_atual = pg.time.get_ticks()
        # Controla o tempo de recarga dos ataques:
        if self.__attacking:
            if tempo_atual - self.__attack_time >= self.__attack_cd:
                self.__attacking = False

    def animate(self):
        animation = self.animations[self.__status]

        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(animation):
            self.__frame_index = 0

        self.image = animation[int(self.__frame_index)]

    def update(self):
        self.input()
        self.move()
        self.cooldowns()
        self.status()
        self.animate()

    def renderizar(self):
        self.__janela.blit(self.image, self.__pos)
