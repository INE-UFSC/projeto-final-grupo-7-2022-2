import pygame as pg
from configuracoes import Configuracoes


class BombaDeAsma(pg.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.tipo_sprite = 'bomba_asma'

        self.__configuracoes = Configuracoes()
        self.__escala = self.__configuracoes.tamanhotile

        # Raio em que o jogador deve ficar para coletar o item
        self.__raio_coletar = self.__escala * 0.7

        # Define o retângulo que representa o item
        self.__cor = (0,255,127)
        self.image = pg.Surface((self.__escala, self.__escala))
        self.image.fill(self.__cor)
        self.rect = self.image.get_rect(topleft = pos)

    def get_distancia_direcao_jogador(self, jogador):
        vetor_bombinha = pg.math.Vector2(self.rect.center)
        vetor_jogador = pg.math.Vector2(jogador.rect.center)
        distancia = (vetor_jogador - vetor_bombinha).magnitude()

        if distancia > 0:
            direcao = (vetor_jogador - vetor_bombinha).normalize()
        else:
            direcao = pg.math.Vector2()
        return (distancia, direcao)

    # Atualiza o objeto, verificando a proximidade do player
    def bomba_asma_update(self, jogador):
        distancia = self.get_distancia_direcao_jogador(jogador)[0]
        if distancia <= self.__raio_coletar:
            self.kill()

    def atualizar(self, eventos: list):
        raise NotImplementedError("Atualizar não implementado")

    def renderizar(self):
        raise NotImplementedError("Renderizar não implementado")
