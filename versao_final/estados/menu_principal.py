import sys
from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao_texto_rotacionado import BotaoTextoRotacionado
from configuracoes import Configuracoes
from controlador_de_musica import ControladorDeMusica

from .estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuPrincipal(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__controle_de_musica = ControladorDeMusica()
        self.__tela = pg.display.get_surface()

        self.__imagens = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'menu_principal.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))
        self.__titulo = self.__configuracoes.fonte_titulo.render('Super Lamparina Arfante', True, (255, 255, 255))
        self.__titulo_rect = self.__titulo.get_rect()
        self.__botao_off = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_off.png'))
        self.__botao_on = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_on.png'))

        self.__botao_jogar = BotaoTextoRotacionado((75, 150), (self.__botao_off, self.__botao_on), 'Jogar')
        self.__botao_jogar.no_clique(self.__evento_botao_jogar_clicado)
        self.__botao_opcoes = BotaoTextoRotacionado((75, 290), (self.__botao_off, self.__botao_on), 'Opções')
        self.__botao_opcoes.no_clique(self.__evento_botao_opcoes_clicado)
        self.__botao_creditos = BotaoTextoRotacionado((75, 430), (self.__botao_off, self.__botao_on), 'Créditos')
        self.__botao_creditos.no_clique(self.__evento_botao_creditos_clicado)
        self.__botao_sair = BotaoTextoRotacionado((75, 570), (self.__botao_off, self.__botao_on), 'Sair')
        self.__botao_sair.no_clique(self.__evento_botao_sair_clicado)


    def iniciar(self):
        self.__controle_de_musica.parar_musica()
        self.__controle_de_musica.iniciar_musica(self.__configuracoes.musica_menu)


    def desenhar(self):
        self.__titulo_rect.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 10)
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__titulo, self.__titulo_rect)
        self.__botao_jogar.desenhar()
        self.__botao_opcoes.desenhar()
        self.__botao_creditos.desenhar()
        self.__botao_sair.desenhar()

    def __evento_botao_jogar_clicado(self):
        self._maquina_de_estado.mover_para_estado('menu_registro')

    def __evento_botao_opcoes_clicado(self):
        self._maquina_de_estado.mover_para_estado('menu_opcoes')

    def __evento_botao_creditos_clicado(self):
        self._maquina_de_estado.mover_para_estado('menu_creditos')
        self.__controle_de_musica.som_click()

    def __evento_botao_sair_clicado(self):
        pg.quit()
        sys.exit()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_jogar.atualizar(evento)
                self.__botao_creditos.atualizar(evento)
                self.__botao_opcoes.atualizar(evento)
                self.__botao_sair.atualizar(evento)
