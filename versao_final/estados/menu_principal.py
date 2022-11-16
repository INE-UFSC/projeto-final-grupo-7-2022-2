from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
# from botao import Botao


class MenuPrincipal(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()
        # self.__botao_play = Botao()
        # self.__botao_creditos = Botao()
        # self.__botao_opcoes = Botao()
        # self.__botao_sair = Botao()

        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_principal.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        self.__titulo = self.__configuracoes.fonte_titulo.render('Super Lamparina Arfante', True, (0, 0, 0))
        self.__titulo_rect = self.__titulo.get_rect()

    def desenhar(self):
        self.__titulo_rect.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 10)
        self.__superficie.blit(self.__imagens, (0, 0))
        self.__superficie.blit(self.__titulo, self.__titulo_rect)


    def atualizar(self, eventos: list, delta_time: float):
        raise NotImplementedError("Atualizar não implementado")
