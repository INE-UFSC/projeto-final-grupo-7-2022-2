from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao


class MenuPrincipal(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()

        self.__botao_play = Botao((75, 150), 300, 100)
        self.__botao_opcoes = Botao((72, 310), 260, 80)
        self.__botao_creditos = Botao((72, 430), 260, 100)
        self.__botao_sair = Botao((75, 580), 260, 90)

        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_principal.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        self.__titulo = self.__configuracoes.fonte_titulo.render('Super Lamparina Arfante', True, (0, 0, 0))
        self.__titulo_rect = self.__titulo.get_rect()

    def desenhar(self):
        self.__titulo_rect.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 10)
        self.__superficie.blit(self.__imagens, (0, 0))
        self.__superficie.blit(self.__titulo, self.__titulo_rect)
        # self.__superficie.blit(self.__botao_play.desenhar(), (75, 150))
        # self.__superficie.blit(self.__botao_opcoes.desenhar(), (75, 310))
        # self.__superficie.blit(self.__botao_creditos.desenhar(), (75, 430))
        # self.__superficie.blit(self.__botao_sair.desenhar(), (75, 580))

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_play.atualizar()
        self.__botao_creditos.atualizar()
        self.__botao_opcoes.atualizar()
        self.__botao_sair.atualizar()

        if self.__botao_play.status == 'clicado':
            self.maquina_de_estado.mover_para_estado('menu_registro')
            self.__botao_play.status = 'nao_clicado'
        elif self.__botao_creditos.status == 'clicado':
            self.maquina_de_estado.mover_para_estado('menu_creditos')
            self.__botao_creditos.status = 'nao_clicado'
        elif self.__botao_opcoes.status == 'clicado':
            self.maquina_de_estado.mover_para_estado('menu_opcoes')
            self.__botao_opcoes.status = 'nao_clicado'
        elif self.__botao_sair.status == 'clicado':
            pass
