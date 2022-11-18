from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao


class MenuCreditos(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()

        self.__botao_back = Botao((1080, 600), 200, 80)
        
        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_creditos.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
    
    def desenhar(self):
        self.__superficie.blit(self.__imagens, (0, 0))
        # self.__superficie.blit(self.__botao_back.desenhar(), (1080, 600))

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_back.atualizar()
        if self.__botao_back.status == 'clicado':
            self.maquina_de_estado.mover_para_estado('menu_principal')
            self.__botao_back.status = 'nao_clicado'
