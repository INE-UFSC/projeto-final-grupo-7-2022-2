import pygame as pg
from abc import ABC, abstractmethod
from .entidade import Entidade


class Inimigo(Entidade):
    def __init__(self, fase, pos):
        super().__init__(fase, pos)
        self.__escala = self.configuracoes.tamanho_tile

        self.status = 'right_idle'
        self.__tipo_sprite = 'inimigo'

        self.__raio_ataque = None
        self.__raio_percepcao = None

        self.__pode_atacar = True
        self.__tempo_ataque = None
        self.__tempo_de_recarga_ataque = None

    @property
    def escala(self):
        return self.__escala

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
    def raio_ataque(self, raio):
        self.__raio_ataque = raio

    @property
    def raio_percepcao(self):
        return self.__raio_percepcao

    @raio_percepcao.setter
    def raio_percepcao(self, raio_percepcao):
        self.__raio_percepcao = raio_percepcao

    @property
    def tempo_ataque(self):
        return self.__tempo_ataque

    @tempo_ataque.setter
    def tempo_ataque(self, tempo_ataque):
        self.__tempo_ataque = tempo_ataque

    @property
    def tempo_de_recarga_ataque(self):
        return self.__tempo_de_recarga_ataque

    @tempo_de_recarga_ataque.setter
    def tempo_de_recarga_ataque(self, tempo_de_recarga_ataque):
        self.__tempo_de_recarga_ataque = tempo_de_recarga_ataque

    @property
    def tipo_sprite(self):
        return self.__tipo_sprite

    def obter_status(self, jogador):
        # Pega a distância do player e o inimigo
        distancia = self.pegar_distancia_direcao_jogador(jogador)[0]

        if distancia <= self.raio_ataque and self.pode_atacar:
            if self.status != 'attack':
                self.status = 'attack'
        elif distancia <= self.raio_percepcao:
            self.status = 'move'
        else:
            self.status = 'right_idle'

    def tempos_de_recarga(self):
        tempo_atual = pg.time.get_ticks()
        if not self.__pode_atacar:
            if tempo_atual - self.__tempo_ataque >= self.__tempo_de_recarga_ataque:
                self.__pode_atacar = True

    @abstractmethod
    def pegar_distancia_direcao_jogador(self, jogador):
        pass

    def acoes(self, player):
        if self.status == 'attack':
            self.tempo_ataque = pg.time.get_ticks()
            # ajeitar
            # self.dano_no_jogador()
            self.pode_atacar = False
        elif self.status == 'move':
            self.direction = self.pegar_distancia_direcao_jogador(player)[1]
        else:
            self.direction = pg.math.Vector2()
