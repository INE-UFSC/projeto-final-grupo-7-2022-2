from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from botao_volume import BotaoVolume
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
        self.__tamanho_botao_volume = (600, 200)
        self.__nivel_musica = self.__musica_control.volume_musica
        self.__nivel_som = self.__musica_control.volume_som

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_folha_off.png')),(self.__configuracoes.tamanho_botoes[0] + 25, self.__configuracoes.tamanho_botoes[1]))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_folha_on.png')),(self.__configuracoes.tamanho_botoes[0] + 25, self.__configuracoes.tamanho_botoes[1]))

        self.__volume_musica = [pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_musica_0.png')),(self.__tamanho_botao_volume)),
                                pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_musica_1.png')),(self.__tamanho_botao_volume)),
                                pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_musica_2.png')),(self.__tamanho_botao_volume)),
                                pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_musica_3.png')),(self.__tamanho_botao_volume))]

        self.__volume_som = [pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_som_0.png')),(self.__tamanho_botao_volume)),
                             pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_som_1.png')),(self.__tamanho_botao_volume)),
                             pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_som_2.png')),(self.__tamanho_botao_volume)),
                             pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'volume_som_3.png')),(self.__tamanho_botao_volume))]

        self.__botao_volume_musica = BotaoVolume((75, 100),self.__volume_musica)
        self.__botao_volume_musica.no_clique(self.__evento_botao_volume_musica_clicado)
        self.__botao_volume_musica.volume = self.__nivel_musica

        self.__botao_volume_som = BotaoVolume((75, 350),self.__volume_som)
        self.__botao_volume_som.no_clique(self.__evento_botao_volume_som_clicado)
        self.__botao_volume_som.volume = self.__nivel_som

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

    def iniciar(self):
        self.__musica_control.parar_musica()
        self.__musica_control.iniciar_musica(self.__configuracoes.musica_opcoes)        

    def __evento_botao_voltar_clicado(self):
        self._maquina_de_estado.voltar()
        #self.__musica_control.som_click()

    def __evento_botao_volume_musica_clicado(self):
        self.__musica_control.mudar_volume_musica()

        if self.__nivel_musica >= 3:
            self.__nivel_musica = 0
        else:
            self.__nivel_musica += 1

        self.__botao_volume_musica.volume = self.__nivel_musica

    def __evento_botao_volume_som_clicado(self):
        self.__musica_control.mudar_volume_som()

        if self.__nivel_som >= 3:
            self.__nivel_som = 0
        else:
            self.__nivel_som += 1
        
        self.__botao_volume_som.volume = self.__nivel_som

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__botao_voltar.desenhar()
        self.__botao_volume_musica.desenhar()
        self.__botao_volume_som.desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar()
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
                self.__botao_volume_musica.atualizar(evento)
                self.__botao_volume_som.atualizar(evento)
