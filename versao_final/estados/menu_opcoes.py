from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from configuracoes import Configuracoes
from controlador_de_musica import ControladorDeMusica
from estados.estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuOpcoes(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__musica_control = ControladorDeMusica()
        self.__tela = pg.display.get_surface()

        self.__botao_off = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_off.png'))
        self.__botao_on = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_on.png'))

        self.__botao_voltar = Botao((1080, 580), (self.__botao_off, self.__botao_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__evento_botao_voltar_clicado)
        self.__imagens = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'menu_opcoes.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))

        self.__botao_volume_musica = Botao((75, 150), (self.__botao_off, self.__botao_on), '')
        self.__botao_volume_musica.no_clique(self.__evento_botao_volume_musica_clicado)

    def __evento_botao_voltar_clicado(self):
        self._maquina_de_estado.voltar()
        self.__musica_control.som_click()

    def __evento_botao_volume_musica_clicado(self):
        self.__musica_control.mudar_volume_musica()

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__botao_voltar.desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar()
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
                self.__botao_volume_musica.atualizar(evento)
