from os import path
from typing import TYPE_CHECKING, List, Tuple

import pygame as pg

from configuracoes import Configuracoes
from superficie_posicionada import SuperficiePosicionada

if TYPE_CHECKING:
    from fase import Fase


class Flecha():
    def __init__(self, fase: 'Fase', posicao: pg.Vector2, direcao: pg.Vector2) -> None:

        super().__init__()

        self.__fase = fase
        self.__configuracoes = Configuracoes()

        # Imagem
        self.__tamanho = pg.Vector2(16, 3) * self.__configuracoes.tamanho_tile * 0.05
        self.__imagem = pg.transform.scale(pg.image.load(path.join('recursos', 'sprites', 'flecha.png')), self.__tamanho)
        self.__rect = self.__imagem.get_rect(center=posicao)
        self.__posicao = pg.Vector2(self.__rect.center)
        # Movimento
        self.__direcao = direcao

    def __atualizar_posicao(self, tempo_passado: int) -> pg.Vector2:
        # Transforma o comprimento do vetor em 1
        velocidade = 0.5
        # Move a bala baseado na direção e velocidade
        return self.__posicao + self.__direcao * (velocidade * tempo_passado)

    def __verificar_colisao(self, nova_posicao: pg.Vector2) -> bool:
        linha = (self.__posicao, nova_posicao)

        objetos_colididos: List[Tuple[Tuple[int, int], 'Jogador' | None]] = []
        dano = 10
        jogador = self.__fase.jogador
        if alvo_posicao_colisao := jogador.hitbox.clipline(linha):
            objetos_colididos.append((alvo_posicao_colisao[0], jogador))

        for colisor in self.__fase.colisores:
            if alvo_posicao_colisao := colisor.rect.clipline(linha):
                objetos_colididos.append((alvo_posicao_colisao[0], None))

        objetos_colididos.sort(key=lambda x: self.__posicao.distance_to(x[0]))
        if len(objetos_colididos) > 0:
            alvo_posicao_colisao, alvo = objetos_colididos[0]
            if alvo is not None:
                alvo.receber_dano(dano)
            return True
        return False

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        return (SuperficiePosicionada(self.__imagem, pg.Vector2(self.__rect.topleft)),)

    def atualizar(self, tempo_passado: int) -> bool:
        nova_posicao = self.__atualizar_posicao(tempo_passado)
        colidiu = self.__verificar_colisao(nova_posicao)
        self.__posicao = nova_posicao
        self.__rect.center = nova_posicao

        return colidiu
