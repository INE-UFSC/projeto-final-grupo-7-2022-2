from os import path
import pygame as pg
from configuracoes import Configuracoes
from estados.estado import Estado
from botao import Botao
from entrada_texto_usuario import EntradaTextoUsuario
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class MenuRegistro(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__configuracoes = Configuracoes()
        self.__tela = pg.display.get_surface()
        imagem_botao_off = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_off.png'))
        imagem_botao_on = pg.image.load(path.join('recursos', 'imagens', 'botao_bandeira_on.png'))

        self.__botao_voltar = Botao((10, 350), (imagem_botao_off, imagem_botao_on), 'Voltar')
        self.__botao_voltar.no_clique(self.__evento_botao_voltar_clicado)
        self.__botao_registro = Botao((1050, 330), (imagem_botao_off, imagem_botao_on), 'Iniciar')
        self.__botao_registro.no_clique(self.__evento_botao_registro_clicado)

        posicao_entrade_usuario = pg.Vector2(370, 370)
        self.__entrada_usuario = EntradaTextoUsuario(posicao_entrade_usuario, largura=550, altura=100)

        self.__imagens = pg.transform.scale(
            pg.image.load(
                path.join(
                    'recursos',
                    'imagens',
                    'registro.png')),
            (self.__configuracoes.largura_tela,
             self.__configuracoes.altura_tela))

        self.__clique_registro = 0
        self.__mostra_mensagem = False
        self.__duracao_mensagem = 2000

    def __evento_botao_voltar_clicado(self):
        self.__entrada_usuario.texto_usuario = ''
        self._maquina_de_estado.mover_para_estado('menu_principal')

    def __evento_botao_registro_clicado(self):
        self.__clique_registro = pg.time.get_ticks()
        if self.__entrada_usuario.texto_usuario:
            self._maquina_de_estado.mover_para_estado('partida')
        else:
            self.__mostra_mensagem = True

    def mostrar_mensagem(self) -> None:
        atual = pg.time.get_ticks()
        if self.__mostra_mensagem:
            mensagem = self.__configuracoes.fonte_botao.render('Por favor, digite o seu nome!', True, (255, 255, 255))
            msg_rect = mensagem.get_rect()
            msg_rect.center = (self.__configuracoes.largura_tela // 2, (self.__configuracoes.altura_tela // 4) * 3)
            self.__tela.blit(mensagem, msg_rect)
        if atual - self.__clique_registro > self.__duracao_mensagem:
            self.__mostra_mensagem = False

    def desenhar(self) -> None:
        self.__tela.blit(self.__imagens, (0, 0))
        self.__botao_voltar.desenhar()
        self.__botao_registro.desenhar()
        self.__entrada_usuario.desenhar()
        self.mostrar_mensagem()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        for evento in eventos:
            if evento.type == pg.QUIT:
                self._maquina_de_estado.sair_do_jogo()
            elif evento.type == pg.MOUSEBUTTONDOWN or evento.type == pg.MOUSEMOTION:
                self.__botao_voltar.atualizar(evento)
                self.__botao_registro.atualizar(evento)
        self.__entrada_usuario.atualizar(eventos)
