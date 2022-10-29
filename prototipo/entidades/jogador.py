from curses import KEY_DOWN
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

        # self.image = pg.transform.scale(pg.image.load('sprites/player.png').convert_alpha(), (self.__escala, self.__escala))
        self.__spritesheet = Spritesheet("player", 2)
        self.image = self.__spritesheet.get_sprite("idle_0.png")
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -4)

        self.__obstacle_sprites = obstacle_sprites
        
        self.__velocidade = 5
        self.__direction = pg.math.Vector2()

        self.__sentido = "Baixo"
        self.__janela = screen
        self.__faca = Faca()
        self.__pistola = Pistola()
    
    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.__direction.y = -1
            self.__sentido = "Cima"
        elif keys[pg.K_DOWN]:
            self.__direction.y = 1
            self.__sentido = "Baixo"
        else:
            self.__direction.y = 0
            self.__sentido = "Baixo"

        if keys[pg.K_RIGHT]:
            self.__direction.x = 1
            self.__sentido = "Direita"
        elif keys[pg.K_LEFT]:
            self.__direction.x = -1
            self.__sentido = "Esquerda"
        else:
            self.__direction.x = 0
            #self.__sentido = "Baixo"

        if keys[pg.K_SPACE]:
            self.__pistola.usar_arma(self.__janela, self.rect.x, self.rect.y, self.__escala, self.__sentido)

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

    @property
    def animations(self):
        # Dicionary containg animation states and their steps.
        animation_dict = {} 
        spr_list = self.__sprite_sheet.sprite_list
        
        for spr in spr_list:
            spr = spr
            spr_info = spr.split("_") # Separa o nome da sprite em um estado e um passo e coloca eles numa lista.
            state = spr_info[0] # Indica o estado da animação (idle, run, hit, etc)
            step = spr_info[1][1:] # Indica o passo da animação (0, 1, 2, ...)

            if state not in animation_dict:
                animation_dict.update(state, list(step))
            else:
                animation_dict[state] += step

            return animation_dict

    def update(self):
        self.input()
        self.move()

    def renderizar(self):
        self.__janela.blit(self.image, self.__pos)
