import pygame as pg, sys
from configuracoes import Configuracoes
from maquina_de_estado import MaquinaDeEstado
from entidades.jogador import Jogador


class Jogo:
    def __init__(self):
        self.__configuracoes = Configuracoes()
        # self.__maquina_de_estado = MaquinaDeEstado()

        # Inicia o pygame e define a janela
        pg.init()
        self.screen = pg.display.set_mode((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        pg.display.set_caption('SUPER LAMPARINA ARFANTE') 

        self.timer = pg.time.Clock()

    def run(self):
        jogador = Jogador((self.__configuracoes.largura_tela/2)-25,(self.__configuracoes.altura_tela/2)-35)
        run = True
        while run:
            self.screen.fill('black')
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    sys.exit()
            
            jogador.renderizar(self.screen)
            jogador.atualizar()

            pg.display.update()
            self.timer.tick()
