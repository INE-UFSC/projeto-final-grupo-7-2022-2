from typing import Tuple, TYPE_CHECKING

import pygame as pg

from superficie_posicionada import SuperficiePosicionada

if TYPE_CHECKING:
    from fase import Fase


class Flecha():
    def __init__(self, fase: 'Fase', posicao: pg.Vector2, direcao: pg.Vector2) -> None:

        super().__init__()

        self.__fase = fase

        # Imagem
        self.__tamanho = (800, 8000)
        self.__superficie = pg.Surface(self.__tamanho)
        self.__superficie.fill((255, 128, 0))
        self.__rect = self.__superficie.get_rect(center=posicao)

        # Movimento
        self.__direcao = direcao

    def __mover(self, tempo_passado: int) -> None:
        # Transforma o comprimento do vetor em 1
        velocidade = 0.5
        # Move a bala baseado na direção e velocidade
        self.__rect.center += self.__direcao * (velocidade * tempo_passado)

    def __verificar_colisao(self) -> bool:

        if self.__fase.jogador.hitbox.colliderect(self.__rect):
            self.__fase.jogador.receber_dano(10)
            return True

        for colisor in self.__fase.colisores:
            if colisor.rect.colliderect(self.__rect):
                return True

        return False

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        return (SuperficiePosicionada(self.__superficie, self.__rect.topleft),)

    def atualizar(self, tempo_passado: int) -> bool:
        self.__mover(tempo_passado)
        return self.__verificar_colisao()
