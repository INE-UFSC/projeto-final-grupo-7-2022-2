from os import path
from typing import TYPE_CHECKING, List

import pygame as pg
from math import ceil

from visualizacao import Botao
from utilidades import Configuracoes, ControladorDeMusica
from .estado import Estado


if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuRanking(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = pg.display.get_surface()
        self.__controle_de_musica = ControladorDeMusica()

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_nuvem_off.png')), (self.__configuracoes.tamanho_botoes))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_nuvem_on.png')), (self.__configuracoes.tamanho_botoes))

        self.__botao_voltar = Botao((1095, 580), (self.__botao_off, self.__botao_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__evento_botao_voltar_clicado)

        self.__botao_off_pagina = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_off.png')), (370, 75))
        self.__botao_on_pagina = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_final_on.png')), (370, 75))

        self.__botao_pagina_anterior = Botao((200, 640), (self.__botao_off_pagina, self.__botao_on_pagina), 'Página Anterior')
        self.__botao_pagina_anterior.no_clique(self.__evento_botao_pagina_anterior_clicado)

        self.__botao_pagina_seguinte = Botao((690, 640), (self.__botao_off_pagina, self.__botao_on_pagina), 'Página Seguinte')
        self.__botao_pagina_seguinte.no_clique(self.__evento_botao_pagina_seguinte_clicado)

        # Aqui deverá ser colocado o que for escrito na tela
        self.__texto = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.__a_ser_desenhado = []
        self.__pagina_atual = 1
        self.__quant_pag = 1
        self.__posicao_inicial = (self.__configuracoes.largura_tela // 6, self.__configuracoes.altura_tela // 6)

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

    def __evento_botao_pagina_anterior_clicado(self):
        if self.__pagina_atual > 1:
            self.__pagina_atual -= 1

    def __evento_botao_pagina_seguinte_clicado(self):
        if self.__pagina_atual < self.__quant_pag:
            self.__pagina_atual += 1

    def desenhar(self):
        self.__tela.blit(self.__imagens, (0, 0))
        self.__tela.blit(self.__filtro, (0, 0))

        texto_tela = self.__configuracoes.fonte_titulo.render('Ranking', True, (255, 255, 255))
        texto = texto_tela.get_rect()
        texto.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 12)
        self.__tela.blit(texto_tela, texto)

        cont_pag = self.__configuracoes.fonte_botao.render(f'{self.__pagina_atual}/{self.__quant_pag}', True, (255, 255, 255))
        cont = cont_pag.get_rect()
        cont.center = (self.__configuracoes.largura_tela // 2, 11 * self.__configuracoes.altura_tela // 12)
        self.__tela.blit(cont_pag, cont)

        # Texto
        if len(self.__texto) > 0:
            texto_render = []
            for linha in self.__texto:
                texto_render.append(self.__configuracoes.fonte_botao.render(linha, True, (255, 255, 255)))
            
            espaco_desenho = 500
            altura_texto = texto_render[0].get_height()
            altura_total = ((altura_texto + 15)* len(texto_render))
            ultima_linha = 0

            self.__a_ser_desenhado = []
            for i in range(0, int(ceil(altura_total / espaco_desenho))):
                self.__a_ser_desenhado.append([])
                for n in range(ultima_linha, len(texto_render)):
                    if ((n - ultima_linha) * (altura_texto + 15)) + altura_texto > espaco_desenho:
                        ultima_linha = n
                        break
                    else:
                        self.__a_ser_desenhado[i].append(texto_render[n])

            if len(self.__a_ser_desenhado) > 0:
                self.__quant_pag = len(self.__a_ser_desenhado)

            self.desenhar_ranking(self.__a_ser_desenhado)

        self.__botao_voltar.desenhar()
        self.__botao_pagina_anterior.desenhar()
        self.__botao_pagina_seguinte.desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
                self.__botao_pagina_anterior.atualizar(evento)
                self.__botao_pagina_seguinte.atualizar(evento)
            elif evento.type == pg.KEYDOWN:
                if evento.key == pg.K_ESCAPE:
                    self._maquina_de_estado.voltar()

    def desenhar_ranking(self, lista):
        pag_atual = self.__a_ser_desenhado[self.__pagina_atual - 1]
        altura_texto = pag_atual[0].get_height()
        for i in range(len(pag_atual)):
            self.__tela.blit(pag_atual[i], (self.__posicao_inicial[0], self.__posicao_inicial[1] + ((i) * altura_texto) + ((i) * 15)))
