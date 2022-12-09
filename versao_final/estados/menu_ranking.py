from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from configuracoes import Configuracoes
from estados.estado import Estado
from controlador_de_musica import ControladorDeMusica


if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuRanking(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = pg.display.get_surface()
        self.__controle_de_musica = ControladorDeMusica()

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_nuvem_off.png')),(self.__configuracoes.tamanho_botoes))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_nuvem_on.png')),(self.__configuracoes.tamanho_botoes))

        self.__botao_voltar = Botao((1080, 580), (self.__botao_off, self.__botao_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__evento_botao_voltar_clicado)

        self.__imagens = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'menu_ranking.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))

        self.__filtro = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'filtro_ranking.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))

    def iniciar(self):
        self.__controle_de_musica.parar_musica()
        self.__controle_de_musica.iniciar_musica(self.__configuracoes.musica_ranking)

    def __evento_botao_voltar_clicado(self):
        self._maquina_de_estado.voltar()
        self.__controle_de_musica.som_botao("nuvem")

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__filtro, (0,0))
        self.__botao_voltar.desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar()
