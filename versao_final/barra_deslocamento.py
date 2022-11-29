import pygame as pg
from os import path
from configuracoes import Configuracoes

class BarraDeslocamento:
    def __init__(self, altura):
        self.__configuracoes = Configuracoes()

        self.__altura = altura
        self.__eixo_y = 0
        self.__mudar_y = 0

        altura_barra = int((self.__configuracoes.altura_tela - 40) / (self.__altura / (self.__configuracoes.altura_tela * 1.0)))
        self.__ret_barra = pg.Rect(self.__configuracoes.largura_tela - 20,20,20,altura_barra)
        self.__seta_sobe = pg.Rect(self.__configuracoes.largura_tela - 20,0,20,20)
        self.__seta_desce = pg.Rect(self.__configuracoes.largura_tela - 20,self.__configuracoes.altura_tela - 20,20,20)
        
        self.__imagem_sobe = pg.image.load(path.join('recursos', 'imagens', 'sobe.png')).convert()
        self.__imagem_desce = pg.image.load(path.join('recursos', 'imagens', 'desce.png')).convert()
        
        self.__na_barra = False
        self.__diferenca_mouse = 0
        
    @property
    def eixo_y(self):
        return self.__eixo_y

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, altura):
        self.__altura = altura

    def atualizar(self, eventos):
        for evento in eventos:
            # Subida e descda com o mouse interagindo com a barra e com os botões
            if evento.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if self.__ret_barra.collidepoint(pos):
                    self.__diferenca_mouse = pos[1] - self.__ret_barra.y
                    self.__na_barra = True
                elif self.__seta_sobe.collidepoint(pos):
                    self.__mudar_y = 5
                elif self.__seta_desce.collidepoint(pos):
                    self.__mudar_y = -5
                    
            if evento.type == pg.MOUSEBUTTONUP:
                self.__mudar_y = 0
                self.__na_barra = False
            
            # Descida e subida com as setas do teclado
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_UP:
                    self.__mudar_y = 5
                elif evento.key == pg.K_DOWN:
                    self.__mudar_y = -5
                    
            if evento.type == pg.KEYUP:
                if evento.key == pg.K_UP:
                    self.__mudar_y = 0
                elif evento.key == pg.K_DOWN:
                    self.__mudar_y = 0

        self.__eixo_y += self.__mudar_y
        
        if self.__eixo_y > 0:
            self.__eixo_y = 0
        elif (self.__eixo_y + self.__altura) < self.__configuracoes.altura_tela:
            self.__eixo_y = self.__configuracoes.altura_tela - self.__altura
            
        diferenca_altura = self.__altura - self.__configuracoes.altura_tela
        
        scroll_length = self.__configuracoes.altura_tela - self.__ret_barra.height - 40
        bar_half_lenght = self.__ret_barra.height / 2 + 20
        
        if self.__na_barra:
            pos = pg.mouse.get_pos()
            self.__ret_barra.y = pos[1] - self.__diferenca_mouse
            if self.__ret_barra.top < 20:
                self.__ret_barra.top = 20
            elif self.__ret_barra.bottom > (self.__configuracoes.altura_tela - 20):
                self.__ret_barra.bottom = self.__configuracoes.altura_tela - 20
            
            self.__eixo_y = int(diferenca_altura / (scroll_length * 1.0) * (self.__ret_barra.centery - bar_half_lenght) * -1)
        else:
            self.__ret_barra.centery =  scroll_length / (diferenca_altura * 1.0) * (self.__eixo_y * -1) + bar_half_lenght
                
    def desenhar(self,superficie):
        pg.draw.rect(superficie,(197, 194, 197),self.__ret_barra)
        
        superficie.blit(self.__imagem_sobe,(self.__configuracoes.largura_tela - 20,0))
        superficie.blit(self.__imagem_desce,(self.__configuracoes.largura_tela - 20,self.__configuracoes.altura_tela - 20))
            