import pygame as pg
from configuracoes import Configuracoes
from mapa import Mapa, Tile
from entidades.jogador import Jogador
from entidades.ladino import Ladino
from bomba_de_asma import BombaDeAsma


class Fase:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

        self.__configuracoes = Configuracoes()

        # Dois grupos de sprites, as que estão visíveis e as que são obstáculos
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        # Outros grupos de sprites para facilitar a verificacao de colisao e dano
        self.attack_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()

        # Cria o mapa baseado em um arquivo csv
        self.__mapa = Mapa('mapa_teste16x16.csv')
        self.create_map()

    def registrar_evento(self, tipo, callback: callable):
        raise NotImplementedError("Registrar evento não implementado")

    def terminar_fase(self):
        raise NotImplementedError("Terminar fase não implementado")

    def create_map(self):
        for row_index, row in enumerate(self.__mapa.mapa):
            for col_index, col in enumerate(row):
                x = col_index * self.__configuracoes.tamanhotile
                y = row_index * self.__configuracoes.tamanhotile
                
                #Faz as substituições dos sprites com base no arquivo csv
                if col == 'PLAYER':
                    self.__jogador = Jogador((x, y), [self.visible_sprites], self.obstacle_sprites, self.display_surface)
                elif col == 'parede':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'ladino':
                    Ladino((x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.dano_no_jogador)
                elif col == 'bomba_asma':
                    BombaDeAsma((x, y), [self.visible_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'inimigo':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def dano_no_jogador(self, quantidade):
        if self.__jogador.vulneravel:
            self.__jogador.vida -= quantidade
            self.__jogador.vulneravel = False
            # Define o momento que o jogador sofreu o dano
            self.__jogador.hurt_time = pg.time.get_ticks()
    
    # Desenha a quantidade de vidas restantes do player
    def barra_de_vida(self):
        escala = self.__configuracoes.tamanhotile * 1.5
        coracao_imagem = pg.image.load('sprites/coracao.png').convert_alpha()
        coracao_imagem = pg.transform.scale(coracao_imagem, (escala, escala))
        for c in range(self.__jogador.vida):
            self.display_surface.blit(coracao_imagem, (c * 50, 0))

    # Função para encerrar o jogo caso o jogador esteja morto
    def encerra_jogo(self):
        if self.__jogador.morto:
            return True
    
    def run(self, screen):
        #Desenha as sprites visíveis e atualiza elas
        self.visible_sprites.bomba_asma_update(self.__jogador)
        self.visible_sprites.custom_draw(self.__jogador)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.__jogador)
        self.barra_de_vida()
        self.player_attack_logic()
        

class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display_surface = pg.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pg.math.Vector2()

    def custom_draw(self, player):
        # Offset é o deslocamento que a posição dos sprites visíveis deve ter para simular uma câmera
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        # Ao invés de desenharmos os objetos numa posição fixa, nos os posicionamos de acordo com a posição do jogador.
        # Essa posição sempre segue uma disntância fixa do jogador.
        # Além disso, a ordem de desenho dos objetos na tela é crescente com relação a sua posição y
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, jogador):
        sprites_inimigos = [sprite for sprite in self.sprites() if hasattr(sprite, 'tipo_sprite') and sprite.tipo_sprite == 'inimigo']
        for inimigo in sprites_inimigos:
            inimigo.enemy_update(jogador)

    def bomba_asma_update(self, jogador):
        for sprite in self.sprites():
            if hasattr(sprite, 'tipo_sprite') and sprite.tipo_sprite == 'bomba_asma':
                sprite.bomba_asma_update(jogador)