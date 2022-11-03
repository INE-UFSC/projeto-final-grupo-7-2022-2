import pygame as pg, sys
from configuracoes import Configuracoes
from maquina_de_estado import MaquinaDeEstado
from entidades.jogador import Jogador
from fase import Fase


class Jogo:
    def __init__(self):
        self.__configuracoes = Configuracoes()

        # Inicia o pygame e define a janela
        pg.init()
        self.screen = pg.display.set_mode((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        pg.display.set_caption('SUPER LAMPARINA ARFANTE') 

        self.timer = pg.time.Clock()
        self.fase = Fase()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            if self.fase.encerra_jogo():
                pg.quit()
                sys.exit()
            
            self.screen.fill('black')
            self.fase.run(self.screen)
            pg.display.update()
            self.timer.tick(self.__configuracoes.fps)
