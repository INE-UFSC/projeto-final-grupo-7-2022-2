from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao
from controlador_de_music import Controlador_de_Musica
import random


class MenuCreditos(Estado):
    def __init__(self, maquina_de_estado, tela):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__musica_control = Controlador_de_Musica()
        self.__tela = tela
        self.__superficie = pg.display.get_surface()
        self.__nuvens_x = random.randrange(0, self.__configuracoes.largura_tela - 300, 10)
        self.__nuvens_y = self.__configuracoes.altura_tela
        self.__altura = 300
        self.__velocidade = random.randrange(1, 5, 1)
        self.__incremento = 100
        self.__last = pg.time.get_ticks()
        self.__cooldowm = random.randrange(0, 6000, 1000)

        self.__botao_off = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_off.png'))
        self.__botao_on = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_on.png'))

        self.__botao_voltar = Botao((1080, 600), (self.__botao_off, self.__botao_on), 'Voltar')
        self.__botao_voltar.on_click(self.__evento_botao_voltar_clicado)
        
        self.__imagens = [pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_creditos.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela)), pg.transform.scale(pg.image.load(path.join('recursos', 'imagens', 'menu_creditos_nomes.png')), (self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))]
        self.__nuvens = [pg.image.load(path.join('recursos', 'imagens', 'Nuvem1.png')),pg.image.load(path.join('recursos', 'imagens', 'Nuvem2.png')), pg.image.load(path.join('recursos', 'imagens', 'Nuvem3.png')), pg.image.load(path.join('recursos', 'imagens', 'Nuvem4.png')), pg.image.load(path.join('recursos', 'imagens', 'Nuvem5.png'))]
        self.__nuvem_text = ['Nuvem1.png', 'Nuvem2.png', 'Nuvem3.png', 'Nuvem4.png', 'Nuvem5.png']

        self.__musica_control.parar_musica()
        self.__musica_control.iniciar_musica(self.__configuracoes.musica_creditos)
        self.__nuvem_atual = random.randrange(0, 4, 1)

    def __mover_nuvem(self):
        if self.__nuvens_y > -300 and self.__nuvens_x < self.__configuracoes.largura_tela:
            self.__nuvens_y -= self.__velocidade
            self.__incremento += 2
            self.__nuvens[self.__nuvem_atual] = pg.transform.scale(self.__nuvens[self.__nuvem_atual], (self.__altura+self.__incremento, self.__altura))
            
        else:
            self.__nuvens_y = self.__configuracoes.altura_tela
            self.__nuvens[self.__nuvem_atual] =  pg.image.load(path.join('recursos', 'imagens', self.__nuvem_text[self.__nuvem_atual]))
            self.__nuvens_x = random.randrange(0, self.__configuracoes.largura_tela - 300, 10)
            self.__velocidade = 6
            self.__incremento = 0
            self.__cooldowm = random.randrange(0, 6000, 1000)
            self.__last = pg.time.get_ticks()
            self.__nuvem_atual = random.randrange(0, 4, 1)

    def __gerar_nuvem(self):
        now = pg.time.get_ticks()
        if now > self.__last + self.__cooldowm:
            self.__mover_nuvem()
    
    def __evento_botao_voltar_clicado(self):
        self.maquina_de_estado.voltar()
        self.__musica_control.som_click()
        
    def desenhar(self):
        self.__superficie.blit(self.__imagens[0], (0, 0))
        self.__superficie.blit(self.__nuvens[self.__nuvem_atual], (self.__nuvens_x, self.__nuvens_y))
        self.__superficie.blit(self.__imagens[1], (0, 0))
        self.__botao_voltar.desenhar(self.__superficie)

    def atualizar(self, eventos: list, delta_time: float):
        self.__botao_voltar.atualizar()
        self.__gerar_nuvem()