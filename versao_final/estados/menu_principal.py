from os import path
import pygame as pg
import sys
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao
from controlador_de_music import Controlador_de_Musica

class MenuPrincipal(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__musica_control = Controlador_de_Musica()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()

        self.__botao_jogar = Botao((75, 150), 300, 100)
        self.__botao_jogar.on_click(self.__evento_botao_jogar_clicado)
        self.__botao_opcoes = Botao((72, 310), 260, 80)
        self.__botao_opcoes.on_click(self.__evento_botao_opcoes_clicado)
        self.__botao_creditos = Botao((72, 430), 260, 100)
        self.__botao_creditos.on_click(self.__evento_botao_creditos_clicado)
        self.__botao_sair = Botao((75, 580), 260, 90)
        self.__botao_sair.on_click(self.__evento_botao_sair_clicado)

        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_principal.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        self.__titulo = self.__configuracoes.fonte_titulo.render('Super Lamparina Arfante', True, (0, 0, 0))
        self.__titulo_rect = self.__titulo.get_rect()

    def desenhar(self):
        self.__titulo_rect.center = (self.__configuracoes.largura_tela // 2, self.__configuracoes.altura_tela // 10)
        self.__superficie.blit(self.__imagens, (0, 0))
        self.__superficie.blit(self.__titulo, self.__titulo_rect)
        # self.__botao_jogar.desenhar(self.__superficie)
        # self.__botao_opcoes.desenhar(self.__superficie)
        # self.__botao_creditos.desenhar(self.__superficie)
        # self.__botao_sair.desenhar(self.__superficie)

    def __evento_botao_jogar_clicado(self):
        self.maquina_de_estado.mover_para_estado('menu_registro')
    
    def __evento_botao_opcoes_clicado(self):
        self.maquina_de_estado.mover_para_estado('menu_opcoes')
        
    def __evento_botao_creditos_clicado(self):
        self.maquina_de_estado.mover_para_estado('menu_creditos')
        self.__musica_control.som_click()
        
    def __evento_botao_sair_clicado(self):
        pg.quit()
        sys.exit()

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_jogar.atualizar()
        self.__botao_creditos.atualizar()
        self.__botao_opcoes.atualizar()
        self.__botao_sair.atualizar()