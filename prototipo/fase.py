from mapa import Mapa, Tile
from entidades.jogador import Jogador
import pygame as pg
from configuracoes import Configuracoes

class Fase:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

        self.__configuracoes = Configuracoes()

        #Cria dois grupos de sprites, as que estão visíveis e as que são obstáculos
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pg.sprite.Group()

        #Cria o mapa baseado em um arquivo csv
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
                    

    def run(self, screen):
        #Desenha as sprites visíveis e atualiza elas
        self.visible_sprites.custom_draw(self.__jogador)
        self.visible_sprites.update()


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