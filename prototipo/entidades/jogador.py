import pygame as pg
from configuracoes import Configuracoes
from entidades.arma.faca import Faca
from entidades.arma.pistola import Pistola
from spritesheet import Spritesheet
from .entidade import Entidade


class Jogador(Entidade):
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

        self.obstacle_sprites = obstacle_sprites
        
        # Movimento
        self.velocidade = 5
        
        self.vida = 3
        self.vulneravel = True
        self.hurt_time = None
        self.duracao_invencibilidade = 300
        self.morto = False

        # Dash
        self.__dashing = False
        self.__dash_duration = 100
        self.__active_dash = True
        self.__dash_cd = 1000
        self.__dash_time = None

        # Ataque
        self.__attacking = False
        self.__attack_cd = 400
        self.__attack_time = None

        # Animação
        self.__status = 'right'
        
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
            self.direction.y = -1

        elif keys[pg.K_DOWN]:
            self.direction.y = 1

        else:
            self.direction.y = 0

        if keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.__status = "right"
        elif keys[pg.K_LEFT]:
            self.direction.x = -1
            self.__status = "left"
        else:
            self.direction.x = 0

        # Entradas de ataque:
        if keys[pg.K_SPACE] and not self.__attacking:
            self.__attacking = True
            self.__attack_time = pg.time.get_ticks()
            self.__pistola.usar_arma(self.__janela, self.rect.x, self.rect.y, self.__escala, self.__status)

        # Entrada do dash:
        if keys[pg.K_s] and not self.__dashing:
            self.__dashing = True
            self.__dash_time = pg.time.get_ticks()
            self.dash()
            self.__active_dash = False

    def status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.__status and not 'attack' in self.__status:
                self.__status += '_idle'
        else:
            if 'idle' in self.__status:
                self.__status = self.__status.replace('_idle','')
            

        if self.__attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.__status:
                if 'idle' in self.__status:
                    self.__status = self.__status.replace('_idle','_attack')
                else:
                    self.__status += '_attack'
        else:
            if 'attack' in self.__status:
                self.__status = self.__status.replace('_attack', '')

    def dash(self):
        if self.__dashing and self.__active_dash:
            self.velocidade = 20
    
    def cooldowns(self):
        current_time = pg.time.get_ticks()
        # Controla o tempo de recarga dos ataques:
        if self.__attacking:
            if current_time - self.__attack_time >= self.__attack_cd:
                self.__attacking = False

        if self.__dashing:
            if current_time - self.__dash_time >= self.__dash_duration:
                self.__dashing = False
                self.velocidade = 5
        if not self.__active_dash:
            if current_time - self.__dash_time >= self.__dash_cd:
                self.__active_dash = True

        if not self.vulneravel:
            if current_time - self.hurt_time >= self.duracao_invencibilidade:
                self.vulneravel = True

    def animate(self):
        animation = self.animations[self.__status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

        # Oscila a visibilidade quando é atacado
        if not self.vulneravel:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def dar_dano(self):
        return 60

    def check_death(self):
        if self.vida <= 0:
            self.morto = True
            self.kill()

    def update(self):
        self.input()
        self.move()
        self.cooldowns()
        self.status()
        self.animate()
        self.check_death()

    def renderizar(self):
        self.__janela.blit(self.image, self.__pos)
