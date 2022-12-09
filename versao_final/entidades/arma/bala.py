from typing import TYPE_CHECKING, List, Tuple

import pygame as pg

from configuracoes import Configuracoes
from superficie_posicionada import SuperficiePosicionada

if TYPE_CHECKING:
    from entidades import Entidade
    from fase import Fase


class Bala():
    def __init__(self, fase: 'Fase', posicao: pg.Vector2, direcao: pg.Vector2) -> None:
        super().__init__()

        self.__fase = fase
        self.__configuracoes = Configuracoes()

        # Imagem
        self.__tamanho = pg.Vector2(2, 2) * self.__configuracoes.tamanho_tile * 0.05
        self.__superficie = pg.Surface(self.__tamanho)
        self.__superficie.fill((255, 255, 255))
        self.__rect = self.__superficie.get_rect(center=posicao)
        self.__posicao = pg.Vector2(self.__rect.topleft)
        # Movimento
        self.__direcao = direcao

    def tipo(self) -> str:
        return 'bala'

    def __atualizar_posicao(self, tempo_passado: int) -> pg.Vector2:
        # Move a bala baseado na direção e velocidade
        velocidade = 2
        return (self.__posicao + self.__direcao * (velocidade * tempo_passado))

    def __verificar_colisao(self, nova_posicao) -> bool:
        linha = (self.__posicao, nova_posicao)
        entidades_colididas: List[Tuple[Tuple[int, int], 'Entidade' | None]] = []
        dano = 5
        for alvo in self.__fase.entidades:
            if alvo.tipo != 'jogador':
                if alvo_posicao_colisao := alvo.hitbox.clipline(linha):
                    entidades_colididas.append((alvo_posicao_colisao[0], alvo))
        for colisor in self.__fase.colisores:
            if alvo_posicao_colisao := colisor.rect.clipline(linha):
                entidades_colididas.append((alvo_posicao_colisao[0], None))
        
        entidades_colididas.sort(key=lambda x: self.__posicao.distance_to(x[0]))
        if len(entidades_colididas) > 0:
            alvo_posicao_colisao, alvo = entidades_colididas[0]
            if alvo is not None:
                alvo.receber_dano(dano)
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
        nova_posicao = self.__atualizar_posicao(tempo_passado)
        colidiu = self.__verificar_colisao(nova_posicao)
        self.__posicao = nova_posicao
        self.__rect.topleft = self.__posicao.x, self.__posicao.y
        return colidiu
    
