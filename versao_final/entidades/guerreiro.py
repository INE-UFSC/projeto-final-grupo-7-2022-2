from .entidade import Entidade
import pygame as pg
from configuracoes import Configuracoes
from spritesheet import Spritesheet


class Guerreiro(Entidade):
    def __init__(self, fase, pos):
        super().__init__()
        self.__fase = fase
        self.__configuracoes = Configuracoes()
        self.__escala = self.configuracoes.tamanho_tile

        # Informacoes Inimigo
        self.__velocidade = 2
        self.__raio_ataque = 20
        self.__raio_percepcao = 300
        self.__vida = 3

        self.__pode_atacar = True
        self.__tempo_ataque = None
        self.__tempo_de_recarga_ataque = 6 * self.__configuracoes.tps

        # Configurações de gráfico - Ainda estão provisórias
        self.__tipo_sprite = 'inimigo'
        self.__status = 'right_idle'
        self.__cor = (255, 255, 0)
        self.__image = pg.Surface((self.escala, self.escala))
        self.__image.fill(self.cor)

        # Movimento
        self.__rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(0, -10)
        self.__obstacle_sprites = fase.colisores

    @property
    def tipo(self):
        return "guerreiro"

    @property
    def configuracoes(self):
        return self.__configuracoes

    @configuracoes.setter
    def configuracoes(self, configuracoes):
        self.__configuracoes = configuracoes

    @property
    def tempo_de_recarga_ataque(self):
        return self.__tempo_de_recarga_ataque

    @tempo_de_recarga_ataque.setter
    def tempo_de_recarga_ataque(self, tempo_de_recarga_ataque):
        self.__tempo_de_recarga_ataque = tempo_de_recarga_ataque

    @property
    def cor(self):
        return self.__cor

    @cor.setter
    def cor(self, cor):
        self.__cor = cor

    @property
    def escala(self):
        return self.__escala

    @escala.setter
    def escala(self, escala):
        self.__escala = escala

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

    # Calcula a distância e a direção que o jogador está
    def pegar_distancia_direcao_jogador(self, jogador):
        vetor_inimigo = pg.math.Vector2(self.rect.center)
        vetor_jogador = pg.math.Vector2(jogador.rect.center)
        distancia = (vetor_jogador - vetor_inimigo).magnitude()

        if distancia > 0:
            direcao = (vetor_jogador - vetor_inimigo).normalize()
        else:
            direcao = pg.math.Vector2()
        return (distancia, direcao)

    def get_status(self, jogador):
        # Pega a distância do player e o inimigo
        distancia = self.pegar_distancia_direcao_jogador(jogador)[0]

        if distancia <= self.raio_ataque and self.pode_atacar:
            if self.status != 'attack':
                self.status = 'attack'
        elif distancia <= self.raio_percepcao:
            self.status = 'move'
        else:
            self.status = 'right_idle'

    def actions(self, player):
        if self.status == 'attack':
            self.tempo_ataque = pg.time.get_ticks()
            self.dano_no_jogador()
            self.pode_atacar = False
        elif self.status == 'move':
            self.direction = self.pegar_distancia_direcao_jogador(player)[1]
        else:
            self.direction = pg.math.Vector2()

    def animate(self):
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def tempos_de_recarga(self):
        tempo_atual = pg.time.get_ticks()
        if not self.pode_atacar:
            if tempo_atual - self.tempo_ataque >= self.tempo_de_recarga_ataque:
                self.pode_atacar = True

    def toma_dano(self):
        self.__vida -= 1
        if self.__vida <= 0:
            self.kill()

    def atualizar(self, tempo_passado):
        self.move(tempo_passado)
        self.get_status(self.__fase.jogador)
        self.actions(self.__fase.jogador)
        self.animate()
        self.tempos_de_recarga()

    def desenhar(self):
        return (self,)