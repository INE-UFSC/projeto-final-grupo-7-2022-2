import random
from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from configuracoes import Configuracoes
from controlador_de_musica import ControladorDeMusica
from estados.estado import Estado
from controlador_de_musica import ControladorDeMusica

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuPausa(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__controle_de_musica = ControladorDeMusica()
        self.__tela = pg.display.get_surface()

        botao_superficie_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_off.png')),(self.__configuracoes.tamanho_botoes))
        botao_superficie_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_on.png')),(self.__configuracoes.tamanho_botoes))

        self.__botao_voltar = Botao((1080, 600), (botao_superficie_off, botao_superficie_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__voltar_para_jogo)

    def iniciar(self):
        self.__controle_de_musica.parar_musica()
        self.__controle_de_musica.iniciar_musica(self.__configuracoes.musica_creditos)
        self.__jogo_copia = self.__tela.copy()
        self.__jogo_copia.set_alpha(200)

    def desenhar(self):
        self.__tela.fill('black')
        self.__tela.blit(self.__jogo_copia, (0, 0))
        self.__botao_voltar.desenhar()

    def __voltar_para_jogo(self):
        self._maquina_de_estado.voltar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self.__voltar_para_jogo()