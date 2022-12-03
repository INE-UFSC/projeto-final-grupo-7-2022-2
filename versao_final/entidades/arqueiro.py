from typing import TYPE_CHECKING, Tuple, List

import pygame as pg

from configuracoes import Configuracoes
from spritesheet import Spritesheet
from superficie_posicionada import SuperficiePosicionada

from .entidade import Entidade
from .flecha import Flecha
from .inimigo import Inimigo

if TYPE_CHECKING:
    from entidades import Jogador


class Arqueiro(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self._velocidade = 0
        self._raio_ataque = 200
        self._raio_percepcao = 300
        self._vida = 1

        configuracoes = Configuracoes()
        self.__tempo_de_recarga_ataque = 20 * configuracoes.tps
        self.__flechas: List[Flecha] = []

        # Configurações de gráfico - Ainda estão provisórias
        self.__cor = (255, 0, 255)
        self.__superficie = pg.Surface((configuracoes.tamanho_tile, configuracoes.tamanho_tile))
        self.__superficie.fill(self.__cor)

        # Movimento
        self._rect = self.__superficie.get_rect()
        self._hitbox = self.rect.inflate(0, -10)
        self.__linha = pg.surface.Surface((1, 1))
        self.__linha_posicao = (0, 0)

    @property
    def tipo(self) -> str:
        return "arqueiro"

    def __ira_atigir_o_jogador(self, direcao: pg.Vector2) -> bool:
        destino = -direcao.normalize() * self._raio_ataque

        posicao = pg.Vector2(self._rect.center)
        linha = (posicao, posicao + destino)

        self.__linha_posicao = pg.Vector2(min(linha[0].x, linha[1].x), min(linha[0].y, linha[1].y))
        self.__linha = pg.surface.Surface((abs(linha[0].x - linha[1].x), abs(linha[0].y - linha[1].y))).convert_alpha()
        self.__linha.set_colorkey((0, 0, 0))
        pg.draw.line(self.__linha, (0, 255, 128), linha[0] - self.__linha_posicao, linha[1]-self.__linha_posicao, 1)

        objetos_colididos: List[Tuple['Jogador' | None, Tuple[int, int]]] = []

        if jogador_colidido := self._fase.jogador.hitbox.clipline(linha):
            objetos_colididos.append((self._fase.jogador, jogador_colidido[0]))

        for colisor in self._fase.colisores:
            if colisao := colisor.rect.clipline(linha):
                objetos_colididos.append((None, colisao[0]))

        objetos_colididos.sort(key=lambda objeto: posicao.distance_to(objeto[1]))

        if len(objetos_colididos) == 0:
            return False

        if objetos_colididos[0][0] is None:
            return False

        return True

    def __atirar(self) -> None:
        if self._pode_atacar:
            vetor_diferenca = self._calcular_vetor_diferenca_jogador()
            if vetor_diferenca.magnitude() != 0 and self.__ira_atigir_o_jogador(vetor_diferenca):
                flecha = Flecha(self._fase, self._rect.center, -vetor_diferenca.normalize())
                self.__flechas.append(flecha)
                self._pode_atacar = False
                self._fase.esperar_certo_tempo(self.__tempo_de_recarga_ataque, self._ativar_ataque)

    def __atualizar_flechas(self, tempo_passado: int) -> None:
        flechas_que_ainda_nao_terminaram: List[Flecha] = []
        for flecha in self.__flechas:
            chegou_ao_fim = flecha.atualizar(tempo_passado)
            if not chegou_ao_fim:
                flechas_que_ainda_nao_terminaram.append(flecha)
        self.__flechas = flechas_que_ainda_nao_terminaram

    def atualizar(self, tempo_passado: int) -> None:
        super().atualizar(tempo_passado)
        self.__atirar()
        self.__atualizar_flechas(tempo_passado)

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        arqueiro_superficies = (SuperficiePosicionada(self.__superficie, self._rect.topleft),)
        for flecha in self.__flechas:
            arqueiro_superficies += flecha.desenhar()
        arqueiro_superficies += (SuperficiePosicionada(self.__linha, self.__linha_posicao),)
        return arqueiro_superficies
