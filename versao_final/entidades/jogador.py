from typing import TYPE_CHECKING, Tuple

import pygame as pg

from spritesheet import Spritesheet
from superficie_posicionada import SuperficiePosicionada

from .arma import Faca, Pistola
from .entidade import Entidade

if TYPE_CHECKING:
    from fase import Fase


class Jogador(Entidade):
    def __init__(self) -> None:
        super().__init__()

        self.__teclas_usadas_estado = {
            pg.K_w: False,
            pg.K_a: False,
            pg.K_s: False,
            pg.K_d: False,
            pg.K_SPACE: False,
        }

        # Imagem e hitbox
        self.__status = 'right'
        self.__spritesheet = Spritesheet("skelet", 1)
        self.__animacoes = self.__spritesheet.get_animation_frames()
        self.__frame_indice = 0
        self._rect = self.__superficie_atual.get_rect()
        self._hitbox = self._rect.inflate(0, -8)

        # Movimento
        self._velocidade = 5

        self.__vida = 300
        self.__vulneravel = True
        self.hurt_time = None
        self.duracao_invencibilidade = 300
        self.morto = False

        # Dash
        self.__impulso_disponivel = True
        self.__esta_com_impulso = False
        self.__duracao_do_impulso = 100
        self.__duracao_de_recarga_do_impulso = 1000
        self.__tempo_do_impulso = None

        # Ataque
        self.__esta_atacando = False
        self.__attack_cd = 400
        self.__tempo_do_ataque = None
        # Animação

        self.__faca = Faca(self)
        self.__pistola = Pistola(self)

        self.__arma = self.__faca
        self.__faca.ativo = True
        self.__centro_da_tela = self.__calcular_centro_da_tela()

    def __calcular_centro_da_tela(self) -> pg.Vector2:
        largura, altura = pg.display.get_surface().get_size()
        return pg.Vector2(largura // 2, altura // 2)

    @property
    def __superficie_atual(self):
        return self.__animacoes[self.__status][int(self.__frame_indice)]

    @property
    def rect(self):
        return self._rect

    def registrar_na_fase(self, fase: 'Fase') -> None:
        super().registrar_na_fase(fase)
        fase.registrar_evento(pg.KEYUP, self.__evento_tecla_solta)
        fase.registrar_evento(pg.KEYDOWN, self.__evento_tecla_apertada)
        fase.registrar_evento(pg.MOUSEBUTTONDOWN, self.__evento_mouse)
        self.__faca.definir_fase(fase)
        self.__pistola.definir_fase(fase)

    def __calcular_direcao(self):

        if self.__teclas_usadas_estado[pg.K_w] == self.__teclas_usadas_estado[pg.K_s]:
            self._direcao.y = 0
        elif self.__teclas_usadas_estado[pg.K_w]:
            self._direcao.y = -1
        elif self.__teclas_usadas_estado[pg.K_s]:
            self._direcao.y = 1

        if self.__teclas_usadas_estado[pg.K_a] == self.__teclas_usadas_estado[pg.K_d]:
            self._direcao.x = 0
        elif self.__teclas_usadas_estado[pg.K_a]:
            self._direcao.x = -1
        elif self.__teclas_usadas_estado[pg.K_d]:
            self._direcao.x = 1

    def __trocar_arma(self):
        self.__arma.ativo = False
        if self.__arma == self.__faca:
            self.__arma = self.__pistola
        else:
            self.__arma = self.__faca
        self.__arma.ativo = True

    def __calcula_impulso(self):
        if self.__teclas_usadas_estado[pg.K_SPACE] and not self.__esta_com_impulso:
            self.__esta_com_impulso = False
            self.__tempo_do_impulso = pg.time.get_ticks()

    def __evento_tecla_solta(self, evento):
        # Entradas de movimentação:
        if evento.key in self.__teclas_usadas_estado:
            self.__teclas_usadas_estado[evento.key] = False

    def __evento_tecla_apertada(self, evento):
        if evento.key in self.__teclas_usadas_estado:
            self.__teclas_usadas_estado[evento.key] = True
        if evento.key == pg.K_LSHIFT:
            self.__trocar_arma()
        if evento.key == pg.K_r and self.__arma.tipo == 'pistola':
            self.__arma.recarregar()

    def __evento_mouse(self, evento):
        if evento.button == 1:
            self.__atacar()

    @property
    def tipo(self):
        return "jogador"

    # Posição do mouse relativa ao jogador

    def __calcular_posicao_do_mouse_relativa_ao_jogador(self) -> pg.Vector2:
        return pg.Vector2(pg.mouse.get_pos()) - self.__centro_da_tela

    def __calcular_tipo_de_animacao(self, posicao_do_mouse_relativa_ao_jogador: pg.Vector2) -> str:

        # Orientação do personagem com relação ao mouse
        if posicao_do_mouse_relativa_ao_jogador.x > 0:
            if 'right' not in self.__status:
                self.__status = 'right'
        else:
            if 'left' not in self.__status:
                self.__status = 'left'

        # Animação de movimento
        if self._direcao.x == 0 and self._direcao.y == 0:
            if 'idle' not in self.__status and 'attack' not in self.__status:
                self.__status += '_idle'
        else:
            if 'idle' in self.__status:
                self.__status = self.__status.replace('_idle', '')

        # if self.__esta_atacando:
        #     self._direcao.x = 0
        #     self._direcao.y = 0
        #     if not 'attack' in self.__status:
        #         if 'idle' in self.__status:
        #             self.__status = self.__status.replace('_idle', '_attack')
        #         else:
        #             self.__status += '_attack'
        # else:
        #     if 'attack' in self.__status:
        #         self.__status = self.__status.replace('_attack', '')

    def dash(self):
        if self.__dashing and self.__active_dash:
            self.__velocidade = 20

    def cooldowns(self):
        tempo_atual = pg.time.get_ticks()
        # Controla o tempo de recarga dos ataques:
        if self.__esta_atacando:
            if tempo_atual - self.__tempo_do_ataque >= self.__attack_cd:
                self.__esta_atacando = False

        """
        if self.__esta_com_impulso:
            if current_time - self.__dash_time >= self.__dash_duration:
                self.__dashing = False
                self._velocidade = 5
        if not self.__active_dash:
            if current_time - self.__dash_time >= self.__dash_cd:
                self.__active_dash = True
        """

        if not self.__vulneravel:
            if tempo_atual - self.hurt_time >= self.duracao_invencibilidade:
                self.__vulneravel = True

    def __animar(self):
        animacao = self.__animacoes[self.__status]

        self.__frame_indice += self._velocidade_da_animacao
        if self.__frame_indice >= len(animacao):
            self.__frame_indice = 0

        self.image = animacao[int(self.__frame_indice)]

        # Oscila a visibilidade quando é atacado
        if not self.__vulneravel:
            alfa = self.wave_value()
            self.image.set_alpha(alfa)
        else:
            self.image.set_alpha(255)

    def __atacar(self) -> None:
        if not self.__esta_atacando:
            self.__esta_atacando = True

            self.__tempo_do_ataque = pg.time.get_ticks()
            self.__arma.ativo = True

            self.__arma.usar_arma()

    def receber_dano(self, dano: int) -> None:
        if self.__vulneravel:
            self.__vulneravel = False
            self.hurt_time = pg.time.get_ticks()
            self.__vida -= dano
            if self.__vida <= 0:
                self._fase.matar_entidade(self)

    def atualizar(self, tempo_passado: int):
        posicao_do_mouse_relativa_ao_jogador = self.__calcular_posicao_do_mouse_relativa_ao_jogador()
        self.__calcular_direcao()
        self.__calcula_impulso()
        self._mover(tempo_passado)
        self.cooldowns()
        self.__calcular_tipo_de_animacao(posicao_do_mouse_relativa_ao_jogador)
        self.__animar()
        self.__faca.atualizar(posicao_do_mouse_relativa_ao_jogador, tempo_passado)
        self.__pistola.atualizar(posicao_do_mouse_relativa_ao_jogador, tempo_passado)

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        jogador_desenho = SuperficiePosicionada(self.__superficie_atual, self._rect.topleft)
        faca_desenho = self.__faca.desenhar()
        arma_desenho = self.__pistola.desenhar()
        return (jogador_desenho,) + faca_desenho + arma_desenho
