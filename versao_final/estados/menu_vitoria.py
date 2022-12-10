from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from utilidades import Configuracoes, ControladorDeMusica
from visualizacao import Botao

from .estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuVitoria(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = pg.display.get_surface()
        self.__controle_de_musica = ControladorDeMusica()

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_off.png')), (225, 65))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_on.png')), (225, 65))

        self.__botao_sair = Botao((400, 500), (self.__botao_off, self.__botao_on), 'Sair')
        self.__botao_sair.no_clique(self.__evento_botao_iniciar_clicado)

        self.__botao_avancar = Botao((650, 500), (self.__botao_off, self.__botao_on), 'Ranking')
        self.__botao_avancar.no_clique(self.__evento_botao_ranking_clicado)

        self.__imagens = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'vitoria.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))

        self.__filtro = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'filtro.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))

    def iniciar(self):
        self.__controle_de_musica.parar_musica()
        self.__controle_de_musica.iniciar_musica(self.__configuracoes.musica_opcoes)

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__filtro, (-22, 0))
        self.__botao_sair.desenhar()
        self.__botao_avancar.desenhar()

    def __evento_botao_iniciar_clicado(self):
        self._maquina_de_estado.voltar_para_inicio()

    def __evento_botao_ranking_clicado(self):
        self._maquina_de_estado.mover_para_estado('menu_ranking')
        self.__controle_de_musica.som_botao("")

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_sair.atualizar(evento)
                self.__botao_avancar.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar_para_inicio()
