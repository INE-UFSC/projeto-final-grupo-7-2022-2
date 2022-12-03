from typing import TYPE_CHECKING, Callable

import pygame as pg

from configuracoes import Configuracoes
from entidades import Entidade, Jogador
from gerenciador_de_grupos import GerenciadorDeGrupos
from View.camera import Camera

if TYPE_CHECKING:
    from estados import Partida


class Fase:
    def __init__(self, partida: 'Partida', nome: str):

        self.__configuracoes = Configuracoes()

        self.__partida = partida
        self.__nome = nome

        self.__tela = pg.display.get_surface()

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    def iniciar(self, jogador: Jogador) -> None:
        self.__jogador = jogador
        self.__gerenciador_de_grupos = GerenciadorDeGrupos(self, self.__nome)
        self.__camera = Camera(self.__gerenciador_de_grupos)
        for entidade in self.entidades:
            entidade.registrar_na_fase(fase=self)

    def esperar_certo_tempo(self, tempo: int, callback: Callable) -> int:
        return self.__partida.esperar_certo_tempo(tempo, callback)

    def cancelar_esperar_certo_tempo(self, identificador: int) -> None:
        self.__partida.cancelar_esperar_certo_tempo(identificador)

    def registrar_evento(self, tipo: int, callback: Callable) -> int:
        return self.__partida.registrar_evento(tipo, callback)

    def terminar_fase(self):
        self.__partida.terminar_fase()

    def atualizar(self, tempo_passado: int):
        for entidade in self.entidades:
            entidade.atualizar(tempo_passado)

    def desenhar(self) -> None:
        centro_do_desenho = pg.Vector2(self.__jogador.rect.center)
        superficies_para_desenho = []

        for entidade in self.entidades:
            superficies_para_desenho.extend(entidade.desenhar())

        self.__camera.desenhar(centro_do_desenho, superficies_para_desenho)

    def matar_entidade(self, entidade: Entidade) -> None:
        self.__gerenciador_de_grupos.matar_entidade(entidade)
        if entidade is self.__jogador:
            self.__partida.jogo_perdido()

    @property
    def colisores(self):
        return self.__gerenciador_de_grupos.colisores

    @property
    def entidades(self):
        return self.__gerenciador_de_grupos.entidades
