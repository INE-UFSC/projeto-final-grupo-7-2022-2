from .entidade import Entidade
import pygame as pg
from configuracoes import Configuracoes
from spritesheet import Spritesheet


class Ladino(Entidade):
    def __init__(self, fase, pos, groups, obstacle_sprites, dano_no_jogador):
        super().__init__(groups)
        self.__configuracoes = Configuracoes()
        self.__escala = self.configuracoes.tamanho_tile

        # Informacoes Inimigo
        self.__vida = 1
        self.__dano = 1
        self.__velocidade = 4
        self.__resistencia = 3
        self.__raio_ataque = 25
        self.__raio_percepcao = 150

        # Invencibilidade - Para o dano ser único e não multiplicado pelo FPS
        self.__vulneravel = True
        self.__hit_time = None
        self.__duracao_invencibilidade = 300

        self.__dano_no_jogador = dano_no_jogador

        self.__pode_atacar = True
        self.__tempo_ataque = None
        self.__cooldown_ataque = 300

        # Configurações de gráfico - Ainda estão provisórias
        self.__tipo_sprite = 'inimigo'
        self.__status = 'right_idle'
        self.__cor = (255, 0, 0)
        self.__image = pg.Surface((self.escala, self.escala))
        self.__image.fill(self.cor)

        # Movimento
        self.__rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(0, -10)
        self.__obstacle_sprites = obstacle_sprites

    @property
    def tipo(self):
        return "ladino"

    @property
    def configuracoes(self):
        return self.__configuracoes

    @configuracoes.setter
    def configuracoes(self, configuracoes):
        self.__configuracoes = configuracoes

    @property
    def cooldown_ataque(self):
        return self.__cooldown_ataque

    @cooldown_ataque.setter
    def cooldown_ataque(self, cooldown_ataque):
        self.__cooldown_ataque = cooldown_ataque

    @property
    def cor(self):
        return self.__cor

    @cor.setter
    def cor(self, cor):
        self.__cor = cor

    @property
    def dano(self):
        return self.__dano

    @dano.setter
    def dano(self, dano):
        self.__dano = dano

    @property
    def dano_no_jogador(self):
        return self.__dano_no_jogador

    @dano_no_jogador.setter
    def dano_no_jogador(self, dano_no_jogador):
        self.__dano_no_jogador = dano_no_jogador

    @property
    def duracao_invencibilidade(self):
        return self.__duracao_invencibilidade

    @duracao_invencibilidade.setter
    def duracao_invencibilidade(self, duracao_invencibilidade):
        self.__duracao_invencibilidade = duracao_invencibilidade

    @property
    def escala(self):
        return self.__escala

    @escala.setter
    def escala(self, escala):
        self.__escala = escala

    @property
    def hit_time(self):
        return self.__hit_time

    @hit_time.setter
    def hit_time(self, hit_time):
        self.__hit_time = hit_time

    @property
    def hitbox(self):
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, hitbox):
        self.__hitbox = hitbox

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @obstacle_sprites.setter
    def obstacle_sprites(self, obstacle_sprites):
        self.__obstacle_sprites = obstacle_sprites

    @property
    def pode_atacar(self):
        return self.__pode_atacar

    @pode_atacar.setter
    def pode_atacar(self, pode_atacar):
        self.__pode_atacar = pode_atacar

    @property
    def raio_ataque(self):
        return self.__raio_ataque

    @raio_ataque.setter
    def raio_ataque(self, raio_ataque):
        self.__raio_ataque = raio_ataque

    @property
    def raio_percepcao(self):
        return self.__raio_percepcao

    @raio_percepcao.setter
    def raio_percepcao(self, raio_percepcao):
        self.__raio_percepcao = raio_percepcao

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect

    @property
    def resistencia(self):
        return self.__resistencia

    @resistencia.setter
    def resistencia(self, resistencia):
        self.__resistencia = resistencia

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def tempo_ataque(self):
        return self.__tempo_ataque

    @tempo_ataque.setter
    def tempo_ataque(self, tempo_ataque):
        self.__tempo_ataque = tempo_ataque

    @property
    def tipo_sprite(self):
        return self.__tipo_sprite

    @tipo_sprite.setter
    def tipo_sprite(self, tipo_sprite):
        self.__tipo_sprite = tipo_sprite

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

    @property
    def vulneravel(self):
        return self.__vulneravel

    @vulneravel.setter
    def vulneravel(self, vulneravel):
        self.__vulneravel = vulneravel

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

    def actions(self, player):
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
        #animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        # if self.frame_index >= len(animation):
        if self.status == 'attack':  # A linha seguinte é provisória
            # if self.status == 'right':
            self.pode_atacar = False
        self.frame_index = 0

        #self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

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

    def atualizar(self, tempo_passado):
        self.hit_reaction()
        self.move()
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, jogador):
        self.get_status(jogador)
        self.actions(jogador)
