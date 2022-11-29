from estados import Partida
import pygame as pg

from configuracoes import Configuracoes
from View.fase_construtor import FaseConstrutor
from View.camera import Camera

from entidades.jogador import Jogador

class Fase:
    def __init__(self, partida: Partida, nome: str):

        self.__configuracoes = Configuracoes()

        self.__partida = partida
        self.__nome = nome
        
        self.display_surface = pg.display.get_surface()

        # Grupos de elementos da fase
        self.__camera               = Camera()
        self.__colisores            = pg.sprite.Group()
        self.__entidades            = pg.sprite.Group()
        self.attack_sprites         = pg.sprite.Group()
        self.__attackable_sprites   = pg.sprite.Group()
        self.__inimigos             = pg.sprite.Group()
        self.__ameacas              = pg.sprite.Group()

        self.__fase_construtor = FaseConstrutor(self, nome)
        self.gerar_fase()


    def registrar_evento(self, tipo, callback: callable):
        return self.__partida.registrar_evento(tipo, callback)

    def terminar_fase(self):
        self.__partida.terminar_fase()

    # Inclusão de todos os elementos da fase em seus grupos
    def gerar_fase(self):
        self.__fase_construtor.grupos['chao'].add(self.__camera)
        
        for bloco in self.__fase_construtor.grupos['blocos']:
            bloco.add(self.__camera)

        for colisor in self.__fase_construtor.grupos['colisores']:
            colisor.add(self.__colisores)

        # for estrutura in self.__mapa.fase_grupos['estruturas']:
        #     estrutura.add(self.__camera)

        for entidade in self.__fase_construtor.grupos['entidades']:
            entidade.add(self.__camera, self.__entidades)
            if isinstance(entidade, Jogador):
                self.__jogador = entidade


    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                if attack_sprite.ativo and attack_sprite.tipo_sprite != 'flecha':
                    collision_sprites = pg.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                    if collision_sprites:
                        for target_sprite in collision_sprites:
                            if target_sprite.tipo_sprite == 'inimigo':
                                target_sprite.toma_dano()


    # Logica de controle de dano
    def dano_no_jogador(self):
        if self.__jogador.vulneravel:
            self.__jogador.vida -= 1
            self.__jogador.vulneravel = False
            # Define o momento que o jogador sofreu o dano
            self.__jogador.hurt_time = pg.time.get_ticks()


    def atualizar(self, tempo_passado):
        for entidade in self.__entidades.sprites():
            entidade.atualizar(tempo_passado)
            if isinstance(entidade, Jogador):
                self.__jogador = entidade
        self.player_attack_logic()

    def desenhar(self):
        self.display_surface.fill('black')
        self.__camera.desenhar(self.__jogador)

    
    @property
    def colisores(self):
        return self.__colisores

    @property
    def jogador(self):
        return self.__jogador
        