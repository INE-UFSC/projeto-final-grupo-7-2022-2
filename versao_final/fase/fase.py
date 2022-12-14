import os
from typing import TYPE_CHECKING, Callable

import pygame as pg

from entidades import Entidade, Guerreiro, Inimigo, Jogador
from utilidades import Configuracoes
from visualizacao import Transicao

from .camera import Camera
from .gerenciador_de_grupos import GerenciadorDeGrupos
from .tempo import Tempo

if TYPE_CHECKING:
    from estados import Partida


class Fase:
    def __init__(self, partida: 'Partida', nome: str):
        self.__configuracoes = Configuracoes()

        self.__partida = partida
        self.__nome = nome

        self.__tela = pg.surface.Surface((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        self.__tempo_passado = 0

        self.__porta = pg.Rect(640, 64, 128, 64)
        self.__bomba_coletada = None
        self.__tempo_coleta = 0

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    def iniciar(self, jogador: Jogador) -> None:
        self.__jogador = jogador
        self.__gerenciador_de_grupos = GerenciadorDeGrupos(self, self.__nome)
        self.__camera = Camera(self.__gerenciador_de_grupos)
        for entidade in self.entidades:
            entidade.registrar_na_fase(fase=self)
        self.__fase_iniciada = True

    def esperar_certo_tempo(self, tempo: int, callback: Callable) -> int:
        return self.__partida.esperar_certo_tempo(tempo, callback)

    def cancelar_esperar_certo_tempo(self, identificador: int) -> None:
        self.__partida.cancelar_esperar_certo_tempo(identificador)

    def registrar_evento(self, tipo: int, callback: Callable) -> int:
        return self.__partida.registrar_evento(tipo, callback)

    def passar_de_fase(self) -> None:
        if self.__fase_iniciada:
            if self.__jogador.rect.colliderect(self.__porta):
                inimigos = [entidade for entidade in self.entidades if isinstance(entidade, Inimigo)]
                if len(inimigos) == 0:
                    self.__terminar_fase()
                    self.__fase_iniciada = False

    def __terminar_fase(self):
        self.__partida.terminar_fase()

    def atualizar(self, tempo_passado: int):
        for entidade in self.entidades:
            entidade.atualizar(tempo_passado)
        self.passar_de_fase()

    def desenhar(self) -> pg.Surface:
        centro_do_desenho = pg.Vector2(self.__jogador.rect.center)
        superficies_para_desenho = []

        for entidade in self.entidades:
            superficies_para_desenho.extend(entidade.desenhar())

        self.__tela.fill('black')
        self.__tela.blit(self.__camera.desenhar(centro_do_desenho, superficies_para_desenho), (0, 0))
        self.__desenhar_hud()
        return self.__tela

    def __desenhar_hud(self):
        self.__desenhar_vidas_restantes()
        self.__desenhar_balas()

    def matar_entidade(self, entidade: Entidade) -> None:
        self.__gerenciador_de_grupos.matar_entidade(entidade)
        if entidade is self.__jogador:
            self.__partida.jogo_perdido()

    def __desenhar_vidas_restantes(self):
        tamanho = 100
        coracao = pg.transform.scale(pg.image.load(os.path.join('recursos', 'sprites', 'coracao.png')), (tamanho, tamanho))
        meio_coracao = pg.transform.scale(pg.image.load(os.path.join('recursos', 'sprites', 'meio_coracao.png')), (tamanho, tamanho))

        vida_atual = self.__jogador.vida // 10

        if vida_atual % 2 == 0:
            for i in range(vida_atual // 2):
                self.__tela.blit(coracao, (i * tamanho * 0.8, 0))
        else:
            for i in range(vida_atual // 2):
                self.__tela.blit(coracao, (i * tamanho * 0.8, 0))
            tamanho_ultimo = (vida_atual // 2) * tamanho * 0.8
            self.__tela.blit(meio_coracao, (tamanho_ultimo, 0))

    def __desenhar_balas(self):
        tamanho = 75
        bala = pg.transform.scale(pg.image.load(os.path.join('recursos', 'sprites', 'bala_tela.png')), (tamanho, tamanho))
        for i in range(self.__jogador.balas_restantes_da_pistola):
            self.__tela.blit(bala, (i * tamanho * 0.75, self.__configuracoes.altura_tela - 100))

    def adicionar_tempo(self, tempo: int):
        self.__partida.adicionar_tempo(tempo)
        
    @property
    def colisores(self):
        return self.__gerenciador_de_grupos.colisores

    @property
    def entidades(self):
        return self.__gerenciador_de_grupos.entidades
