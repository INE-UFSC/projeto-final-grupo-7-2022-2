from mapa import Mapa, Tile
from entidades.jogador import Jogador
import pygame as pg
from configuracoes import Configuracoes

class Fase:
    def __init__(self):
        self.display_surface = pg.display.get_surface()

        self.__configuracoes = Configuracoes()

        #Cria dois grupos de sprites, as que estão visíveis e as que são obstáculos
        self.visible_sprites = pg.sprite.Group()
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
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
