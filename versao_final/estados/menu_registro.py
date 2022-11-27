from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao
from entrada_texto_usuario import EntradaTextoUsuario


class MenuRegistro(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()

        self.__botao_off = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_off.png'))
        self.__botao_on = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_on.png'))
        
        self.__botao_voltar = Botao((10, 350), 200, 80, (self.__botao_off, self.__botao_on))
        self.__botao_voltar.on_click(self.__evento_botao_voltar_clicado)
        self.__botao_registro = Botao((1050, 330), 250, 80, (self.__botao_off, self.__botao_on))
        self.__botao_registro.on_click(self.__evento_botao_registro_clicado)

        self.__entrada_usuario = EntradaTextoUsuario((370, 370), 550, 100, self.__tela)

        self.__imagens = pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'registro.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))

    def __evento_botao_voltar_clicado(self):
        self.maquina_de_estado.mover_para_estado('menu_principal')
        
    def __evento_botao_registro_clicado(self):
        if self.__entrada_usuario.texto_usuario:
            self.maquina_de_estado.mover_para_estado('partida')

    def desenhar(self):
        self.__superficie.blit(self.__imagens, (0, 0))
        self.__botao_voltar.desenhar(self.__superficie)
        self.__botao_registro.desenhar(self.__superficie)
        self.__entrada_usuario.desenhar(self.__superficie)

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_voltar.atualizar()
        self.__botao_registro.atualizar()
        self.__entrada_usuario.atualizar(eventos)