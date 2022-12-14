from estados import Partida
import pygame as pg
import os
from configuracoes import Configuracoes
from mapa import Mapa, Tile
from entidades.jogador import Jogador
from entidades.ladino import Ladino
from entidades.guerreiro import Guerreiro
from entidades.arqueiro import Arqueiro
from bomba_de_asma import BombaDeAsma
from entidades.arma.pistola import Pistola

class Fase:
    def __init__(self, partida: Partida):

        self.__partida = partida

        self.display_surface = pg.display.get_surface()

        self.__configuracoes = Configuracoes()

        # Dois grupos de sprites, as que estão visíveis e as que são obstáculos
        self.__grupo_de_entidade = YSortCameraGroup()
        self.__grupo_de_obstaculos = pg.sprite.Group()

        # Outros grupos de sprites para facilitar a verificacao de colisao e dano
        self.__attack_sprites = pg.sprite.Group()
        self.__attackable_sprites = pg.sprite.Group()

        # Cria o mapa baseado em um arquivo csv
        self.__mapa = Mapa(os.path.join('mapa_teste16x16.csv'))
        self.criar_mapa()

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

    def registrar_evento(self, tipo, callback: callable):
        return self.__partida.registrar_evento(tipo, callback)

    def terminar_fase(self):
        self.__partida.terminar_fase()

    def criar_mapa(self):
        for row_index, row in enumerate(self.__mapa.mapa):
            for col_index, col in enumerate(row):
                x = col_index * self.__configuracoes.tamanho_tile
                y = row_index * self.__configuracoes.tamanho_tile

                # Faz as substituições dos sprites com base no arquivo csv
                if col == 'player':
                    self.__jogador = Jogador(self,
                                             (x, y),
                                             [self.__grupo_de_entidade],
                                             self.__grupo_de_obstaculos, self.display_surface)
                elif col == 'parede':
                    Tile(self, (x, y), [self.__grupo_de_entidade, self.__grupo_de_obstaculos])
                elif col == 'ladino':
                    Ladino(self, (x, y), [self.__grupo_de_entidade, self.attackable_sprites],
                           self.__grupo_de_obstaculos, self.dano_no_jogador)
                elif col == 'guerreiro':
                    Guerreiro(self, (x, y), [self.__grupo_de_entidade, self.attackable_sprites],
                           self.__grupo_de_obstaculos, self.dano_no_jogador)
                elif col == 'arqueiro':
                    Arqueiro(self, (x, y), [self.__grupo_de_entidade, self.attackable_sprites],
                           self.__grupo_de_obstaculos, self.dano_no_jogador)
                elif col == 'bomba_asma':
                    BombaDeAsma(self, (x, y), [self.__grupo_de_entidade])

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
        self.__grupo_de_entidade.atualizar(tempo_passado)
        self.player_attack_logic()

    def desenhar(self):
        self.display_surface.fill('black')
        self.__grupo_de_entidade.desenhar(self.__jogador)


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display_surface = pg.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pg.math.Vector2()

    def desenhar(self, player):
        # Offset é o deslocamento que a posição dos sprites visíveis deve ter para simular uma câmera
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        # Ao invés de desenharmos os objetos numa posição fixa, nos os posicionamos de acordo com a posição do jogador.
        # Essa posição sempre segue uma disntância fixa do jogador.
        # Além disso, a ordem de desenho dos objetos na tela é crescente com relação a sua posição y
        sprite_para_desenhar = []
        for sprite in self.sprites():
            sprite_para_desenhar.extend(sprite.desenhar())
        
        for sprite in sorted(sprite_para_desenhar, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image, offset_pos)

    def atualizar(self, tempo_passado):
        for entidade in self.sprites():
            entidade.atualizar(tempo_passado)
