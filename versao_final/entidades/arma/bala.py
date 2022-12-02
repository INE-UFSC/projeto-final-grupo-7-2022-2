from typing import Tuple, TYPE_CHECKING

import pygame as pg

from superficie_posicionada import SuperficiePosicionada

if TYPE_CHECKING:
    from fase import Fase


class Bala():
    def __init__(self, fase: 'Fase', posicao: pg.Vector2, direcao: pg.Vector2) -> None:
        super().__init__()

        self.__fase = fase

        # Imagem
        self.__escala = (8, 8)
        self.__superficie = pg.Surface(self.__escala)
        self.__superficie.fill((255, 255, 255))
        self.__rect = self.__superficie.get_rect(center=posicao)

        # Movimento
        self.__direcao = direcao

    def tipo(self) -> str:
        return 'bala'

    def __atualizar_posicao(self, tempo_passado: int) -> None:
        # Move a bala baseado na direção e velocidade
        velocidade = 0.2
        vetor = (pg.Vector2(self.__rect.topleft) + self.__direcao * (velocidade * tempo_passado))
        self.__rect.topleft = vetor.x, vetor.y

    def __verificar_colisao(self) -> bool:
        dano = 5
        for alvo in self.__fase.entidades:
            if alvo.hitbox.colliderect(self.__rect):
                if alvo.tipo != 'jogador':
                    alvo.receber_dano(dano)
                    print(f"Alvo {alvo.tipo} recebeu {dano} de dano da bala")
                    return True
        for colisor in self.__fase.colisores:
            if colisor.rect.colliderect(self.__rect):
                return True
        return False

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        return (SuperficiePosicionada(self.__superficie, self.__rect.topleft),)

    def atualizar(self, tempo_passado: int) -> bool:
        """

        Args:
            tempo_passado (int): tempo passado desde o última atualização

        Returns:
            Bool: Se a bala deve ser destruida
        """
        self.__atualizar_posicao(tempo_passado)
        return self.__verificar_colisao()
