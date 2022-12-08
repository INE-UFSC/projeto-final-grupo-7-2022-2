from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from configuracoes import Configuracoes
from estados.estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuVitoria(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = pg.display.get_surface()

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_off.png')), (225, 65))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_on.png')), (225, 65))

        self.__botao_sair = Botao((400, 500), (self.__botao_off, self.__botao_on), 'Sair')
        self.__botao_sair.no_clique(self.__evento_botao_iniciar_clicado)

        self.__botao_avancar = Botao((650, 500), (self.__botao_off, self.__botao_on), 'Avançar')
        self.__botao_avancar.no_clique(None)

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

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__filtro, (-22,0))
        self.__botao_sair.desenhar()
        self.__botao_avancar.desenhar()

    def __evento_botao_iniciar_clicado(self):
        self._maquina_de_estado.voltar_para_inicio()


    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_sair.atualizar(evento)
                self.__botao_avancar.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar_para_inicio()
