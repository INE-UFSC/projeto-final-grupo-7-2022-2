from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
# from botao import Botao


class FimDeJogo(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()

        # self.__botao_back = Botao()
        # self.__botao_ranking = Botao()
        
        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'fim_de_jogo.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
    
    def desenhar(self):
        self.__superficie.blit(self.__imagens, (0, 0))

    def atualizar(self, eventos: list, delta_time: float):
        raise NotImplementedError("Atualizar não implementado")
