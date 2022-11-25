from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao
from controlador_de_music import Controlador_de_Musica


class MenuOpcoes(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__musica_control = Controlador_de_Musica()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()
        
        self.__botao_voltar = Botao((1080, 580), 200, 80)
        self.__botao_voltar.on_click(self.__evento_botao_voltar_clicado)
        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_opcoes.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))

        self.__botao_volume_musica = Botao((75, 150), 300, 100)
        self.__botao_volume_musica.on_click(self.__evento_botao_volume_musica_clicado)
    
    def __evento_botao_voltar_clicado(self):
        self.maquina_de_estado.voltar()
        self.__musica_control.som_click()

    def __evento_botao_volume_musica_clicado(self):
        self.__musica_control.mudar_volume_musica()
    
    def desenhar(self):
        self.__superficie.blit(self.__imagens, (0, 0))
        # self.__botao_voltar.desenhar(self.__superficie)

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_voltar.atualizar()
        self.__botao_volume_musica.atualizar()
