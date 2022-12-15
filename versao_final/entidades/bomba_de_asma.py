import pygame as pg
from os import path

from utilidades import Configuracoes
from visualizacao import SuperficiePosicionada

from .entidade import Entidade


class BombaDeAsma(Entidade):
    def __init__(self):
        super().__init__()
        self.__escala = self._configuracoes.tamanho_tile

        # Define o retângulo que representa o item
        self.__image = pg.transform.scale(pg.image.load(path.join('recursos', 'sprites', 'bomba.png')), (self.__escala, self.__escala))
        self._rect = self.__image.get_rect()
        self._hitbox = self._rect.inflate(pg.Vector2(0.5, 0.5) * self.__escala)

    @property
    def tipo(self) -> str:
        return "bomba_de_asma"

    def receber_dano(self, dano):
        pass

    # Atualiza o objeto, verificando a proximidade do player
    def atualizar(self, tempo_passado: int):
        if self._fase.jogador:
            if self._fase.jogador.hitbox.colliderect(self.hitbox):
                self._fase.adicionar_tempo(60)
                self._fase.matar_entidade(self)

    def desenhar(self):
        return (SuperficiePosicionada(self.__image, self._rect.topleft),)
