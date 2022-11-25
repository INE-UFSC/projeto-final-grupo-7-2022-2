from estados import Partida
import pygame as pg
import os
from configuracoes import Configuracoes
from View.mapa import Mapa
from View.camera import Camera

from entidades.jogador import Jogador
# from entidades.ladino import Ladino
# from entidades.guerreiro import Guerreiro
# from entidades.arqueiro import Arqueiro
# from bomba_de_asma import BombaDeAsma
# from entidades.arma.pistola import Pistola

class Fase:
    def __init__(self, partida: Partida, nome: str):

        self.__partida = partida
        self.__nome = nome
        self.display_surface = pg.display.get_surface()
        self.__configuracoes = Configuracoes()

        self.__camera = Camera()
        self.__colisores = pg.sprite.Group()
        self.__grupo_de_entidade = pg.sprite.Group()
        self.__attackable_sprites = pg.sprite.Group()
        self.__inimigos = pg.sprite.Group()
        self.__attack_sprites = pg.sprite.Group()

        self.__mapa = Mapa(nome, self)

        self.gerar_fase()

        self.__jogador = Jogador(self, (320,320), [self.__camera, self.__grupo_de_entidade], self.__colisores, self.display_surface)


    def registrar_evento(self, tipo, callback: callable):
        return self.__partida.registrar_evento(tipo, callback)

    def terminar_fase(self):
        self.__partida.terminar_fase()

    def gerar_fase(self):
        self.__mapa.gerar_mapa()


    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                if attack_sprite.ativo and attack_sprite.tipo_sprite != 'flecha':
                    collision_sprites = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                    if collision_sprites:
                        for target_sprite in collision_sprites:
                            if target_sprite.tipo_sprite == 'inimigo':
                                target_sprite.toma_dano()

    def dano_no_jogador(self):
        if self.__jogador.vulneravel:
            self.__jogador.vida -= 1
            self.__jogador.vulneravel = False
            # Define o momento que o jogador sofreu o dano
            self.__jogador.hurt_time = pg.time.get_ticks()

    @property
    def entidades(self):
        return self.__grupo_de_entidade.sprites()

    def atualizar(self, tempo_passado):
        for entidade in self.__grupo_de_entidade.sprites():
            entidade.atualizar(tempo_passado)
        self.player_attack_logic()

    def desenhar(self):
        self.display_surface.fill('black')
        self.__camera.desenhar(self.__jogador)


    # Propriedades
    @property
    def camera(self):
        return self.__camera

    @property
    def grupo_de_entidade(self):
        return self.__grupo_de_entidade

    @property
    def grupo_de_obstaculos(self):
        return self.__grupo_de_obstaculos

    @property
    def attack_sprites(self):
        return self.__attack_sprites

    @property
    def attackable_sprites(self):
        return self.__attackable_sprites

    @property
    def config(self):
        return self.__configuracoes

    @property
    def jogador(self):
        return self.__jogador
