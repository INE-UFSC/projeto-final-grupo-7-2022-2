from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao


class FimDeJogo(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()

        self.__botao_voltar = Botao((430, 500), 200, 80)
        self.__botao_voltar.on_click(self.__evento_botao_iniciar_clicado)
        
        self.__botao_ranking = Botao((670, 500), 200, 80)
        self.__botao_ranking.on_click(self.__evento_botao_ranking_clicado)
        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'fim_de_jogo.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
    
    def desenhar(self):
        self.__superficie.blit(self.__imagens, (0, 0))
        # self.__superficie.blit(self.__botao_back.desenhar(), (430, 500))
        # self.__superficie.blit(self.__botao_ranking.desenhar(), (670, 500))

    def __evento_botao_iniciar_clicado(self):
        self.maquina_de_estado.voltar_para_inicio()
    
    def __evento_botao_ranking_clicado(self):
        self.maquina_de_estado.mover_para_estado('menu_ranking')
        
    
    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_voltar.atualizar()
        self.__botao_ranking.atualizar()

