from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from utilidades import Configuracoes, ControladorDeMusica, Armazenamento
from visualizacao import Botao

from .estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class FimDeJogo(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__controle_de_musica = ControladorDeMusica()
        self.__tela = pg.display.get_surface()
        self.__armazenamento = Armazenamento()

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

    def iniciar(self):
        self.__controle_de_musica.parar_musica()
        self.__controle_de_musica.iniciar_musica(self.__configuracoes.musica_fim)

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__filtro, (-22, 0))

        texto_tela = self.__configuracoes.fonte_botao.render('Você Perdeu!', True, (255, 255, 255))
        texto = texto_tela.get_rect()
        texto.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 3)
        self.__tela.blit(texto_tela, texto)
        registro = self.__armazenamento.ultima_pontuacao

        minutos = int(registro['tempo']) // 60
        segundos = int(registro['tempo']) % 60
        tempo_string = "{0:02}:{1:02}".format(minutos, segundos)

        texto_tempo = self.__configuracoes.fonte_botao.render(f'Tempo: {tempo_string}', True, (255, 255, 255))
        texto_tempo_rect = texto_tempo.get_rect(center=(self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 2))
        self.__tela.blit(texto_tempo, texto_tempo_rect)

        texto_fase = self.__configuracoes.fonte_botao.render(f'Fase: {registro["fase_indice"]+1}', True, (255, 255, 255))
        texto_fase_rect = texto_fase.get_rect(center=texto_tempo_rect.center)
        texto_fase_rect.y += texto_tempo_rect.height + 10
        self.__tela.blit(texto_fase, texto_fase_rect)

        self.__botao_voltar.desenhar()
        self.__botao_ranking.desenhar()

    def __evento_botao_iniciar_clicado(self):
        self._maquina_de_estado.voltar_para_inicio()
        self.__controle_de_musica.som_botao("")

    def __evento_botao_ranking_clicado(self):
        self._maquina_de_estado.mover_para_estado('menu_ranking')
        self.__controle_de_musica.som_botao("")

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
                self.__botao_ranking.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar_para_inicio()
