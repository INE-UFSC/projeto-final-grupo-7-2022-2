import pygame as pg
from .entidade import Entidade
from .inimigo import Inimigo
from configuracoes import Configuracoes
from spritesheet import Spritesheet


class Ladino(Inimigo):
    def __init__(self, fase, pos):
        super().__init__(fase, pos)

        # Informacoes Inimigo
        self.velocidade = 4
        self.raio_ataque = 25
        self.raio_percepcao = 150

        self.tempo_de_recarga_ataque = 10 * self.configuracoes.tps

        # Configurações de gráfico - Ainda estão provisórias
        self.__cor = (255, 0, 0)
        self.__image = pg.Surface((self.escala, self.escala))
        self.__image.fill(self.__cor)

        # Movimento
        self.__rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(0, -10)

    @property
    def tipo(self):
        return "ladino"

    @property
    def hitbox(self):
        return self.__hitbox

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, rect):
        self.__rect = rect

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

    def animate(self):
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def atualizar(self, tempo_passado):
        self.move(tempo_passado)
        self.obter_status(self.fase.jogador)
        self.acoes(self.fase.jogador)
        self.animate()
        self.tempos_de_recarga()