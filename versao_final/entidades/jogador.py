from typing import TYPE_CHECKING, Tuple

import pygame as pg

from utilidades import Configuracoes
from visualizacao import Spritesheet, SuperficiePosicionada
from .arma import Faca, Pistola
from .entidade import Entidade

if TYPE_CHECKING:
    from fase import Fase


class Jogador(Entidade):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self.__vida = kwargs.get('vida', 100)
        # Imagem e hitbox
        self.__status = 'right'
        self.__spritesheet = Spritesheet("lamparina")
        self.__animacoes = self.__spritesheet.get_animation_frames()
        self.__frame_indice = 0
        self._rect = self.__superficie_atual.get_rect()
        self._hitbox = self._rect.inflate(pg.Vector2(-0.5, -0.5) * self._configuracoes.tamanho_tile)

        # Movimento
        self._velocidade = 0.8

        # Flags para cooldown
        self.__duracao_do_impulso = 100
        self.__duracao_de_recarga_do_impulso = 1000

        self.__faca = Faca(self)
        if 'armas' in kwargs:
            self.__pistola = Pistola.apartir_do_dict(kwargs['armas']['pistola'], self)
        else:
            self.__pistola = Pistola(self)

        if kwargs.get('arma', 'faca') == 'faca':
            self.__arma = self.__faca
        else:
            self.__arma = self.__pistola

        self.__arma.ativo = True

        self.__centro_da_tela = self.__calcular_centro_da_tela()

    @property
    def balas_restantes_da_pistola(self):
        return self.__pistola.balas_restantes

    @property
    def tipo(self):
        return "jogador"

    @property
    def vida(self):
        return self.__vida

    def __calcular_centro_da_tela(self) -> pg.Vector2:
        largura, altura = pg.display.get_surface().get_size()
        return pg.Vector2(largura // 2, altura // 2)

    @staticmethod
    def apartir_do_dict(dados: dict) -> 'Jogador':
        return Jogador(**dados)

    def gerar_dict_do_estado(self) -> dict:
        return {
            'arma': self.__arma.tipo,
            'vida': self.__vida,
            'armas': {
                'pistola': self.__pistola.gerar_dict_do_estado(),
            }
        }

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

        self.__teclas_usadas_estado = {
            pg.K_w: False,
            pg.K_a: False,
            pg.K_s: False,
            pg.K_d: False,
            pg.K_SPACE: False,
        }
        self.__vulneravel = True
        self.__pode_atacar = True
        self.__impulso_disponivel = True
        self.__esta_com_impulso = False
        self._velocidade = 0.8

    def __calcular_direcao(self):
        if self.__esta_com_impulso:
            return
        w = self.__teclas_usadas_estado[pg.K_w]
        a = self.__teclas_usadas_estado[pg.K_a]
        s = self.__teclas_usadas_estado[pg.K_s]
        d = self.__teclas_usadas_estado[pg.K_d]
        if w == s:
            self._direcao.y = 0
        elif w:
            self._direcao.y = -1
        elif s:
            self._direcao.y = 1
        if a == d:
            self._direcao.x = 0
        elif a:
            self._direcao.x = -1
        elif d:
            self._direcao.x = 1

    def __trocar_arma(self):
        self.__arma.ativo = False
        if self.__arma == self.__faca:
            self.__arma = self.__pistola
        else:
            self.__arma = self.__faca
        self.__arma.ativo = True

    def __desativar_impulso(self):
        self.__esta_com_impulso = False
        self._velocidade = 0.8

    def __recarregar_impulso(self):
        self.__impulso_disponivel = True

    def __verficar_impulso(self):
        espaco = self.__teclas_usadas_estado[pg.K_SPACE]
        if espaco and self.__impulso_disponivel and self._direcao.magnitude() != 0:
            self.__impulso_disponivel = False
            self.__esta_com_impulso = True
            self._velocidade = 2.5
            duracao_da_recarga = self.__duracao_de_recarga_do_impulso
            self._fase.esperar_certo_tempo(duracao_da_recarga, self.__recarregar_impulso)
            duracao = self.__duracao_do_impulso
            self._fase.esperar_certo_tempo(duracao, self.__desativar_impulso)

    def __evento_tecla_solta(self, evento):
        # Entradas de movimenta????o:
        if evento.key in self.__teclas_usadas_estado:
            self.__teclas_usadas_estado[evento.key] = False

    def __evento_tecla_apertada(self, evento):
        if evento.key in self.__teclas_usadas_estado:
            self.__teclas_usadas_estado[evento.key] = True
        if evento.key == pg.K_LSHIFT:
            self.__trocar_arma()
        # if evento.key == pg.K_r and self.__arma.tipo == 'pistola':
        #     self.__arma.recarregar()

    def __evento_mouse(self, evento):
        if evento.button == 1:
            self.__atacar()

    # Posi????o do mouse relativa ao jogador

    def __calcular_posicao_do_mouse_relativa_ao_jogador(self) -> pg.Vector2:
        return pg.Vector2(pg.mouse.get_pos()) - self.__centro_da_tela

    def __calcular_tipo_de_animacao(self, posicao_do_mouse_relativa_ao_jogador: pg.Vector2) -> str:
        # Orienta????o do personagem com rela????o ao mouse
        if posicao_do_mouse_relativa_ao_jogador.x > 0:
            self.__status = 'right'
        else:
            self.__status = 'left'

        # Anima????o de movimento
        if self._direcao.x == 0 and self._direcao.y == 0:
            self.__status += '_idle'

    # def dash(self):
    #     if self.__dashing and self.__active_dash:
    #         self.__velocidade = 20

    def __animar(self):
        animacao = self.__animacoes[self.__status]

        self.__frame_indice += self._velocidade_da_animacao
        if self.__frame_indice >= len(animacao):
            self.__frame_indice = 0

        self.image = animacao[int(self.__frame_indice)]

        # Oscila a visibilidade quando ?? atacado
        if not self.__vulneravel:
            alfa = self._oscilar_valor()
            self.image.set_alpha(alfa)
        else:
            self.image.set_alpha(255)

    def __ativar_ataque(self):
        self.__pode_atacar = True

    def __atacar(self) -> None:
        if self.__pode_atacar:
            self.__pode_atacar = False
            self.__arma.usar_arma()
            tempo_de_ataque = 400
            self._fase.esperar_certo_tempo(
                tempo_de_ataque,
                self.__ativar_ataque
            )

    def __desativar_invulnerabilidade(self):
        self.__vulneravel = True

    def receber_dano(self, dano: int) -> None:
        if self.__vulneravel:
            duracao_invulnerabilidade = 300
            self.__vulneravel = False
            self.__vida -= dano
            if self.__vida <= 0:
                self._fase.matar_entidade(self)
            else:
                self._fase.esperar_certo_tempo(
                    duracao_invulnerabilidade,
                    self.__desativar_invulnerabilidade
                )

    def atualizar(self, tempo_passado: int):
        posicao_do_mouse_relativa_ao_jogador = self.__calcular_posicao_do_mouse_relativa_ao_jogador()
        self.__calcular_direcao()
        self.__verficar_impulso()
        self._mover(tempo_passado)
        self.__calcular_tipo_de_animacao(posicao_do_mouse_relativa_ao_jogador)
        self.__animar()
        self.__faca.atualizar(posicao_do_mouse_relativa_ao_jogador, tempo_passado)
        self.__pistola.atualizar(posicao_do_mouse_relativa_ao_jogador, tempo_passado)

    def desenhar(self) -> Tuple[SuperficiePosicionada, ...]:
        jogador_desenho = SuperficiePosicionada(self.__superficie_atual, self._rect.topleft)
        faca_desenho = self.__faca.desenhar()
        arma_desenho = self.__pistola.desenhar()
        return (jogador_desenho,) + faca_desenho + arma_desenho
