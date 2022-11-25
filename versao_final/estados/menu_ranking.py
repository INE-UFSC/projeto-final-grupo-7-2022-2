from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao


class MenuRanking(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()
        
        self.__botao_voltar = Botao((1080, 580), 200, 80)
        self.__botao_voltar.on_click(self.__evento_botao_voltar_clicado)
        
        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'pontuacao.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
    
    def __evento_botao_voltar_clicado(self):
        self.maquina_de_estado.voltar()
    
    def desenhar(self):
        self.__superficie.blit(self.__imagens, (0, 0))
        self.__superficie.blit(self.__botao_voltar.desenhar(), (1080, 580))

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_voltar.atualizar()
        