from typing import TYPE_CHECKING, Callable

import pygame as pg
import os

from configuracoes import Configuracoes
from entidades import Entidade, Jogador, Inimigo, Guerreiro, Inimigo, Guerreiro
from gerenciador_de_grupos import GerenciadorDeGrupos
from View.camera import Camera
from tempo import Tempo
from View.transicao import Transicao
from View.transicao import Transicao

if TYPE_CHECKING:
    from estados import Partida


class Fase:
    def __init__(self, partida: 'Partida', nome: str):
        self.__configuracoes = Configuracoes()

        self.__partida = partida
        self.__nome = nome

        self.__tela = pg.surface.Surface((self.__configuracoes.largura_tela, self.__configuracoes.altura_tela))
        self.__tempo_passado = 0
        self.__tempo_maximo = 60

        self.__porta = pg.Rect(640, 192, 64, 64)

    @property
    def jogador(self) -> Jogador:
        return self.__jogador

    def iniciar(self, jogador: Jogador) -> None:
        self.__jogador = jogador
        self.__gerenciador_de_grupos = GerenciadorDeGrupos(self, self.__nome)
        self.__camera = Camera(self.__gerenciador_de_grupos)
        for entidade in self.entidades:
            entidade.registrar_na_fase(fase=self)
        self.__tempo.iniciar()
        self.__fase_iniciada = True

    def esperar_certo_tempo(self, tempo: int, callback: Callable) -> int:
        return self.__partida.esperar_certo_tempo(tempo, callback)

    def cancelar_esperar_certo_tempo(self, identificador: int) -> None:
        self.__partida.cancelar_esperar_certo_tempo(identificador)

    def registrar_evento(self, tipo: int, callback: Callable) -> int:
        return self.__partida.registrar_evento(tipo, callback)

    def passar_de_fase(self) -> None:
        if self.__fase_iniciada:
            if self.__jogador.rect.colliderect(self.__porta):
                inimigos = [entidade for entidade in self.entidades if isinstance(entidade, Inimigo)]
                if len(inimigos) == 0:
                    self.__terminar_fase()
                    self.__fase_iniciada = False

    def __terminar_fase(self):
        self.__partida.terminar_fase()

    def atualizar(self, tempo_passado: int):
        for entidade in self.entidades:
            entidade.atualizar(tempo_passado)
        self.__tempo.retomar()
        self.passar_de_fase()

    def desenhar(self) -> pg.Surface:
        centro_do_desenho = pg.Vector2(self.__jogador.rect.center)
        superficies_para_desenho = []

        for entidade in self.entidades:
            superficies_para_desenho.extend(entidade.desenhar())

        self.__tela.fill('black')
        self.__tela.blit(self.__camera.desenhar(centro_do_desenho, superficies_para_desenho), (0, 0))
        self.__desenhar_hud()
        return self.__tela
    
    def __desenhar_hud(self):
        self.__desenhar_vidas_restantes()
        self.__desenhar_balas()
        self.__desenhar_tempo()
        self.__desenhar_barra_tempo()

    def matar_entidade(self, entidade: Entidade) -> None:
        self.__gerenciador_de_grupos.matar_entidade(entidade)
        if entidade is self.__jogador:
            self.__partida.jogo_perdido()

    def __desenhar_vidas_restantes(self):
        tamanho = 100
        coracao = pg.transform.scale(pg.image.load(os.path.join('recursos', 'sprites', 'coracao.png')), (tamanho, tamanho))
        meio_coracao = pg.transform.scale(pg.image.load(os.path.join('recursos', 'sprites', 'meio_coracao.png')), (tamanho, tamanho))
        
        # A ser concluído: Decidir quantos corações serão usados e esquema de dano
        vida_atual = self.__jogador.vida // 10

        if vida_atual % 2 == 0:
            for i in range(vida_atual // 2):
                self.__tela.blit(coracao, (i * tamanho * 0.8, 0))
        else:
            for i in range(vida_atual // 2):
                self.__tela.blit(coracao, (i * tamanho * 0.8, 0))
            tamanho_ultimo = (vida_atual // 2) * tamanho * 0.8
            self.__tela.blit(meio_coracao, (tamanho_ultimo, 0))

    def __desenhar_balas(self):
        tamanho = 75
        bala = pg.transform.scale(pg.image.load(os.path.join('recursos', 'sprites', 'bala_tela.png')), (tamanho, tamanho))
        # A ser concluído: Pegar o número de balas restantes para o loop
        for i in range(self.__jogador.balas_restantes_da_pistola):
            self.__tela.blit(bala, (i * tamanho * 0.75, self.__configuracoes.altura_tela - 100))

    def __desenhar_barra_tempo(self):
        tempo_restante = self.__tempo.temporizador(self.__tempo_maximo)
        barra = pg.Rect(self.__configuracoes.largura_tela - tempo_restante * 2 - 50, 100, tempo_restante * 2, 30)
        # A ser concuído: Efeitos colaterais no jogador
        if tempo_restante < 1/3 * self.__tempo_maximo:
            pg.draw.rect(self.__tela, (255, 0, 0), barra)
        else:
            pg.draw.rect(self.__tela, (0, 255, 0), barra)

    def __desenhar_tempo(self):
        self.__tempo_passado = int(self.__tempo.ver_tempo())

        minutos = self.__tempo_passado // 60
        segundos = self.__tempo_passado % 60
    
        tempo_string = "{0:02}:{1:02}".format(minutos, segundos)
    
        texto = self.__configuracoes.fonte_digitar.render(tempo_string, True, (255, 255, 255))
        self.__tela.blit(texto, (self.__configuracoes.largura_tela - texto.get_width() - 50, 0))

    def pausar_tempo(self):
        self.__tempo.pausar()

    @property
    def colisores(self):
        return self.__gerenciador_de_grupos.colisores

    @property
    def entidades(self):
        return self.__gerenciador_de_grupos.entidades
