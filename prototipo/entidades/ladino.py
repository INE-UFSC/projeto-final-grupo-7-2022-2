from .entidade import Entidade
import pygame as pg
from configuracoes import Configuracoes
from spritesheet import Spritesheet


class Ladino(Entidade):
    def __init__(self, pos, groups, obstacle_sprites, dano_no_jogador):
        super().__init__(groups)

        # Informacoes Inimigo
        self.vida = 100
        self.dano = 40
        self.velocidade = 4
        self.resistencia = 3
        self.raio_ataque = 25
        self.raio_percepcao = 150

        # Invencibilidade - Para o dano ser único e não multiplicado pelo FPS
        self.vulneravel = True
        self.hit_time = None
        self.duracao_invencibilidade = 300

        self.dano_no_jogador = dano_no_jogador

        self.pode_atacar = True
        self.tempo_ataque = None
        self.cooldown_ataque = 400

        # Configurações de gráfico - Ainda estão provisórias
        self.tipo_sprite = 'inimigo'
        self.status = 'right_idle'
        self.__spritesheet = Spritesheet("skelet", 1)
        self.image = self.image('idle_0.png')
        self.animations = self.__spritesheet.animation_frames

        # Movimento
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

    def image(self, sprite: str):
        return self.__spritesheet.get_sprite(sprite)

    # Calcula a distancia e a direcao que o jogador esta
    def get_distancia_direcao_jogador(self, jogador):
        vetor_inimigo = pg.math.Vector2(self.rect.center)
        vetor_jogador = pg.math.Vector2(jogador.rect.center)
        distancia = (vetor_jogador - vetor_inimigo).magnitude()

        if distancia > 0:
            direcao = (vetor_jogador - vetor_inimigo).normalize()
        else:
            direcao = pg.math.Vector2()
        return (distancia, direcao)

    def get_status(self, jogador):
        # Pega a distancia do player e o inimigo
        distancia = self.get_distancia_direcao_jogador(jogador)[0]
        
        # As cinco linhas seguintes que estão comentadas (que usam attack e move) são as que devem ficar, as que estão logo abaixo (que usam right e left) são apenas provisórias
        if distancia <= self.raio_ataque and self.pode_atacar:
            # if self.status != 'attack':
            if self.status != 'right':
                self.frame_index = 0
            # self.status = 'attack'
            self.status = 'right'
        elif distancia <= self.raio_percepcao:
            # self.status = 'move'
            self.status = 'left'
        else:
            self.status = 'right_idle'

    def actions(self,player):
        # if self.status == 'attack':
        if self.status == 'right':
            self.tempo_ataque = pg.time.get_ticks()
            self.dano_no_jogador(self.dano)
        # if self.status == 'move':
        elif self.status == 'left':
            self.direction = self.get_distancia_direcao_jogador(player)[1]
        else:
            self.direction = pg.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
		
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            # if self.status == 'attack': - A linha seguinte é provisória
            if self.status == 'right':
                self.pode_atacar = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # Oscila a visibilidade quando é atacado
        if not self.vulneravel:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def cooldowns(self):
        tempo_atual = pg.time.get_ticks()
        if not self.pode_atacar:
            if tempo_atual - self.tempo_ataque >= self.cooldown_ataque:
                self.pode_atacar = True

        if not self.vulneravel:
            if tempo_atual - self.hit_time >= self.duracao_invencibilidade:
                self.vulneravel = True
    
    def get_damage(self, jogador):
        if self.vulneravel:
            self.direction = self.get_player_distance_direction(player)[1]
            self.vida -= jogador.dar_dano()
        self.hit_time = pg.time.get_ticks()
        self.vulnerable = False

    def check_death(self):
        if self.vida <= 0:
            self.kill()

    # Se afasta um pouco caso for atingido
    def hit_reaction(self):
        if not self.vulneravel:
            self.direction *= -self.resistencia

    def update(self):
        self.hit_reaction()
        self.move()
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, jogador):
        self.get_status(jogador)
        self.actions(jogador)
