import pygame as pg


class Camera(pg.sprite.Group):
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
