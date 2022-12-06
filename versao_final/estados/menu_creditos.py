import random
from os import path
from typing import TYPE_CHECKING, List

import pygame as pg

from botao import Botao
from configuracoes import Configuracoes
from controlador_de_musica import ControladorDeMusica
from estados.estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuCreditos(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__musica_control = ControladorDeMusica()
        self.__tela = pg.display.get_surface()

        self.__nuvens_x = random.randrange(0, self.__configuracoes.largura_tela - 300, 10)
        self.__nuvens_y = self.__configuracoes.altura_tela
        self.__altura = 300

        self.__velocidade = random.randrange(2, 4, 1)
        self.__incremento = 100

        self.__last = pg.time.get_ticks()
        self.__cooldowm = random.randrange(0, 6000, 1000)

        self.__botao_off = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_nuvem_off.png')),(self.__configuracoes.tamanho_botoes))
        self.__botao_on = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'botao_nuvem_on.png')),(self.__configuracoes.tamanho_botoes))

        self.__botao_voltar = Botao((1080, 600), (self.__botao_off, self.__botao_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__evento_botao_voltar_clicado)

        self.__imagens = [
            pg.transform.scale(
                pg.image.load(
                    path.join(
                        'recursos',
                        'imagens',
                        'menu_creditos.png')),
                (self.__configuracoes.largura_tela,
                 self.__configuracoes.altura_tela)),
            pg.transform.scale(
                pg.image.load(
                    path.join(
                        'recursos',
                        'imagens',
                        'menu_creditos_nomes.png')),
                (self.__configuracoes.largura_tela,
                 self.__configuracoes.altura_tela))]

        self.__nuvens = [
            pg.image.load(
                path.join(
                    'recursos', 'imagens', 'Nuvem1.png')), pg.image.load(
                path.join(
                    'recursos', 'imagens', 'Nuvem2.png')), pg.image.load(
                        path.join(
                            'recursos', 'imagens', 'Nuvem3.png')), pg.image.load(
                                path.join(
                                    'recursos', 'imagens', 'Nuvem4.png')), pg.image.load(
                                        path.join(
                                            'recursos', 'imagens', 'Nuvem5.png'))]

        self.__nuvem_text = ['Nuvem1.png', 'Nuvem2.png', 'Nuvem3.png', 'Nuvem4.png', 'Nuvem5.png']
        self.__nuvem_atual = random.randrange(0, 4, 1)
        self.__nuvem_desenho = self.__nuvens[self.__nuvem_atual]

        self.__musica_control.parar_musica()
        self.__musica_control.iniciar_musica(self.__configuracoes.musica_creditos)

    def __mover_nuvem(self):
        if self.__nuvens_y > - self.__nuvem_desenho.get_height() and self.__nuvens_x < self.__configuracoes.largura_tela:
            self.__incremento += self.__velocidade / 2
            self.__nuvens_y -= self.__velocidade
            self.__nuvem_desenho = pg.transform.scale(
                self.__nuvens[self.__nuvem_atual], (self.__altura + self.__incremento * 0.5, self.__altura + self.__incremento * 0.3))

        else:
            self.__incremento = 0
            self.__nuvem_atual = random.randrange(0, 4, 1)
            self.__nuvens_y = self.__configuracoes.altura_tela
            self.__nuvens_x = random.randrange(0, self.__configuracoes.largura_tela - 300, 10)
            self.__nuvens[self.__nuvem_atual] = pg.image.load(
                path.join('recursos', 'imagens', self.__nuvem_text[self.__nuvem_atual]))

            self.__velocidade = random.randrange(2, 4, 1)
            self.__cooldowm = random.randrange(0, 6000, 1000)
            self.__last = pg.time.get_ticks()

    def __gerar_nuvem(self):
        now = pg.time.get_ticks()
        if now > self.__last + self.__cooldowm:
            self.__mover_nuvem()

    def __evento_botao_voltar_clicado(self):
        self._maquina_de_estado.voltar()
        self.__musica_control.som_click()

    def desenhar(self):
        self.__tela.blit(self.__imagens[0], (0, 0))
        self.__tela.blit(self.__nuvem_desenho, (self.__nuvens_x, self.__nuvens_y))
        self.__tela.blit(self.__imagens[1], (0, 0))
        self.__botao_voltar.desenhar()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
        self.__gerar_nuvem()
