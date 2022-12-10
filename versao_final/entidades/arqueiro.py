from typing import TYPE_CHECKING, List, Tuple

import pygame as pg

from utilidades import Configuracoes, ControladorDeMusica
from visualizacao import Spritesheet, SuperficiePosicionada

from .entidade import Entidade
from .flecha import Flecha
from .inimigo import Inimigo

if TYPE_CHECKING:
    from entidades import Jogador


class Arqueiro(Inimigo):
    def __init__(self):
        super().__init__()

        # Informacoes Inimigo
        self.__configuracoes = Configuracoes()
        self.__controle_de_musica = ControladorDeMusica()

        self._velocidade = 0.6
        self._raio_ataque = 10
        self._raio_percepcao = 20
        self._vida = 1

        self.__frame_indice = 0
        self.__status = 'right'
        self.__spritesheet = Spritesheet("arqueiro")
        self.__animacoes = self.__spritesheet.get_animation_frames()

        self.__tempo_de_recarga_ataque = 1000
        self.__flechas: List[Flecha] = []
        self.__esta_morto = False

        # Configurações de gráfico - Ainda estão provisórias

        # Movimento
        self._rect = self.__superficie_atual.get_rect()
        self._hitbox = self.rect.inflate(0, -10)

    @property
    def tipo(self) -> str:
        return "arqueiro"

    @property
    def __superficie_atual(self):
        return self.__animacoes[self.__status][int(self.__frame_indice)]

    def __calcular_tipo_de_animacao(self, posicao_do_jogador: pg.Vector2) -> str:

        # Orientação do personagem com relação ao mouse
        if posicao_do_jogador.x > 0:
            self.__status = 'right'
        else:
            self.__status = 'left'

        # Animação de movimento
        if self._direcao.x == 0 and self._direcao.y == 0:
            self.__status += '_idle'

    def __ira_atigir_o_jogador(self, direcao: pg.Vector2) -> bool:
        destino = -direcao.normalize() * self._raio_ataque * self.__configuracoes.tamanho_tile

        posicao = pg.Vector2(self._rect.center)
        linha = (posicao, posicao + destino)

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
        if self._pode_atacar and not self.__esta_morto:
            vetor_diferenca = self._calcular_vetor_diferenca_jogador()
            if vetor_diferenca.magnitude() != 0 and self.__ira_atigir_o_jogador(vetor_diferenca):
                flecha = Flecha(self._fase, self._rect.center, -vetor_diferenca.normalize())
                self.__flechas.append(flecha)
                self._pode_atacar = False
                self._fase.esperar_certo_tempo(self.__tempo_de_recarga_ataque, self._ativar_ataque)
                self.__controle_de_musica.som_ataque("flecha")

    def __atualizar_flechas(self, tempo_passado: int) -> None:
        flechas_que_ainda_nao_terminaram: List[Flecha] = []
        for flecha in self.__flechas:
            chegou_ao_fim = flecha.atualizar(tempo_passado)
            if not chegou_ao_fim:
                flechas_que_ainda_nao_terminaram.append(flecha)
        self.__flechas = flechas_que_ainda_nao_terminaram

    def __animar(self) -> None:
        animacao = self.__animacoes[self.__status]

        self.__frame_indice += self._velocidade_da_animacao
        if self.__frame_indice >= len(animacao):
            self.__frame_indice = 0

    def receber_dano(self, dano: int):
        self._vida -= dano
        if self._vida <= 0:
            if len(self.__flechas) == 0:
                self._fase.matar_entidade(self)
            else:
                self.__esta_morto = True
                self._hitbox = pg.Rect(0, 0, 0, 0)
                self._rect = pg.Rect(0, 0, 0, 0)

    def atualizar(self, tempo_passado: int) -> None:
        direcao = self._calcular_vetor_diferenca_jogador()*-1
        self.__calcular_tipo_de_animacao(direcao)
        super().atualizar(tempo_passado)
        self.__atirar()
        self.__atualizar_flechas(tempo_passado)
        if self.__esta_morto and len(self.__flechas) == 0:
            self._fase.matar_entidade(self)
        self.__animar()

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        if not self.__esta_morto:
            arqueiro_superficies = (SuperficiePosicionada(self.__superficie_atual, self._rect.topleft),)
        else:
            arqueiro_superficies = tuple()
        for flecha in self.__flechas:
            arqueiro_superficies += flecha.desenhar()
        return arqueiro_superficies
