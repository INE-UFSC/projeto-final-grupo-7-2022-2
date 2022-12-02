from typing import TYPE_CHECKING, Tuple

import pygame as pg

from configuracoes import Configuracoes
from entidades import Jogador, Entidade
from superficie_posicionada import SuperficiePosicionada
from View.camera import Camera
from gerenciador_de_grupos import GerenciadorDeGrupos

if TYPE_CHECKING:
    from estados import Partida


class Fase:
    def __init__(self, partida: 'Partida', nome: str):

        self.__configuracoes = Configuracoes()

        self.__partida = partida
        self.__nome = nome
        self.__jogador = Jogador()

        self.__tela = pg.display.get_surface()

        self.__gerenciador_de_grupos = GerenciadorDeGrupos(self, nome)
        self.__camera = Camera()
        self.__camera.chao = self.__gerenciador_de_grupos.chao
        self.__camera.estruturas = self.__gerenciador_de_grupos.estruturas
        self.__camera.blocos = self.__gerenciador_de_grupos.blocos

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    def iniciar(self):
        for entidade in self.entidades:
            entidade.registrar_na_fase(fase=self)

    def registrar_evento(self, tipo: int, callback: callable) -> int:
        return self.__partida.registrar_evento(tipo, callback)

    def terminar_fase(self):
        self.__partida.terminar_fase()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                if attack_sprite.ativo and attack_sprite.tipo_sprite != 'flecha':
                    collision_sprites = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                    if collision_sprites:
                        for target_sprite in collision_sprites:
                            if target_sprite.tipo_sprite == 'inimigo':
                                target_sprite.receber_dano()

    # Logica de controle de dano

    def dano_no_jogador(self):
        if self.__jogador.__vulneravel:
            self.__jogador.vida -= 1
            self.__jogador.__vulneravel = False
            # Define o momento que o jogador sofreu o dano
            self.__jogador.hurt_time = pg.time.get_ticks()

    def atualizar(self, tempo_passado: int):
        for entidade in self.entidades:
            entidade.atualizar(tempo_passado)
        # self.player_attack_logic()

    def desenhar(self) -> None:
        centro_do_desenho = pg.Vector2(self.__jogador.rect.center)
        superficies_para_desenho = []

        for entidade in self.entidades:
            superficies_para_desenho.extend(entidade.desenhar())

        self.__camera.desenhar(centro_do_desenho, superficies_para_desenho)

    def matar_entidade(self, entidade: Entidade) -> None:
        self.__gerenciador_de_grupos.matar_entidade(entidade)

    @property
    def colisores(self):
        return self.__gerenciador_de_grupos.colisores

    @property
    def entidades(self):
        return self.__gerenciador_de_grupos.entidades
