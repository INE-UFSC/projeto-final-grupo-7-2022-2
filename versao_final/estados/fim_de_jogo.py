from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from configuracoes import Configuracoes
from estados.estado import Estado

from controlador_de_musica import ControladorDeMusica

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class FimDeJogo(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__controle_de_musica = ControladorDeMusica()
        self.__tela = pg.display.get_surface()

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_off.png')), (225, 75))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_on.png')), (225, 75))

        self.__botao_voltar = Botao((400, 500), (self.__botao_off, self.__botao_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__evento_botao_iniciar_clicado)

        self.__botao_ranking = Botao((650, 500), (self.__botao_off, self.__botao_on), 'Ranking')
        self.__botao_ranking.no_clique(self.__evento_botao_ranking_clicado)
        self.__imagens = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'fim_de_jogo.png')),
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

        self.__controle_de_musica.parar_musica()
        self.__controle_de_musica.iniciar_musica(self.__configuracoes.musica_fim)
        self.__controle_de_musica.mudar_volume_musica()

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__filtro, (-22,0))

        texto_tela = self.__configuracoes.fonte_botao.render('Você Perdeu!', True, (255, 255, 255))
        texto = texto_tela.get_rect()
        texto.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 3)
        self.__tela.blit(texto_tela, texto)

        # Sua pontuação foi - A ser terminado
        texto_tela2 = self.__configuracoes.fonte_botao.render('Sua pontuação foi: ???', True, (255, 255, 255))
        texto2 = texto_tela2.get_rect()
        texto2.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 2)
        self.__tela.blit(texto_tela2, texto2)

        self.__botao_voltar.desenhar()
        self.__botao_ranking.desenhar()

    def __evento_botao_iniciar_clicado(self):
        self._maquina_de_estado.voltar_para_inicio()

    def __evento_botao_ranking_clicado(self):
        self._maquina_de_estado.mover_para_estado('menu_ranking')

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
                self.__botao_ranking.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar_para_inicio()
