from typing import TYPE_CHECKING, Callable, List

import pygame as pg

from entidades import Jogador
from fase import Fase, Tempo
from utilidades import CallbackDeEvento, Configuracoes, ControladorDeMusica, Armazenamento
from visualizacao import Transicao

from .estado import Estado

if TYPE_CHECKING:
    from maquina_de_estado import MaquinaDeEstado


class Partida(Estado):
    def __init__(self, maquina_de_estado: 'MaquinaDeEstado'):
        super().__init__(maquina_de_estado)
        self.__armazenamento = Armazenamento()
        self.__tempo_maximo = 60

        self.__fases = []
        self.__fase_atual_indice = 0
        self.__tem_jogo = False
        self.__musica_control = ControladorDeMusica()
        self.__marcador_de_tempo_para_eventos = 0
        self.__callback_de_eventos = []
        self.__callback_eventos_de_tempo = []
        self.__idenficador_de_evento_indice = 0
        self.__tela = pg.display.get_surface()
        self.__configuracoes = Configuracoes()
        self.__transicao = Transicao()
        self.__ultimo_quadro_fase: pg.Surface | None = None
        self.__fase_ativa = True

    def registrar_evento(self, tipo: int, callback: Callable) -> int:
        identificador = self.__idenficador_de_evento_indice
        callback_de_evento = CallbackDeEvento(identificador, tipo, callback)
        self.__callback_de_eventos.append(callback_de_evento)
        self.__idenficador_de_evento_indice += 1
        return identificador

    def esperar_certo_tempo(self, tempo: int, callback: Callable) -> int:
        identificador = self.__idenficador_de_evento_indice
        tempo = tempo + self.__marcador_de_tempo_para_eventos
        self.__callback_eventos_de_tempo.append((identificador,
                                                 tempo,
                                                 callback))
        self.__idenficador_de_evento_indice += 1
        return identificador

    def cancelar_esperar_certo_tempo(self, identificador: int):
        for i, (id_, tempo, callback) in enumerate(self.__callback_eventos_de_tempo):
            if id_ == identificador:
                self.__callback_eventos_de_tempo.pop(i)
                break

    def remover_registro_de_evento(self, identificador: int):
        for callback_de_evento in self.__callback_de_eventos:
            if callback_de_evento.id == identificador:
                self.__callback_de_eventos.remove(callback_de_evento)
                break

    def registrar_fase(self, fase: 'Fase'):
        self.__fases.append(fase)

    def __desenhar_tempo(self):
        self.__tempo_passado = int(self.__tempo.ver_tempo())

        minutos = self.__tempo_passado // 60
        segundos = self.__tempo_passado % 60

        tempo_string = "{0:02}:{1:02}".format(minutos, segundos)

        texto = self.__configuracoes.fonte_digitar.render(tempo_string, True, (255, 255, 255))
        self.__tela.blit(texto, (self.__configuracoes.largura_tela - texto.get_width() - 50, 0))

    def __desenhar_barra_tempo(self):
        tamanho_maximo = 120
        margem = 3
        escala = 2
        altura = 30
        tempo_restante = min(tamanho_maximo,  max(self.__tempo.temporizador(self.__tempo_maximo), 0))
        barra_fundo = pg.Surface((tamanho_maximo + margem * escala, altura))
        barra_fundo.fill('black')
        barra_fundo.set_alpha(150)
        barra = pg.Surface((tempo_restante * escala, altura - 2 * margem))
        if tempo_restante < tamanho_maximo / 3:
            barra.fill('red')
            for entidade in self.__fases[self.__fase_atual_indice].entidades:
                if entidade.tipo == 'bomba_de_asma':
                    self.__jogador.receber_dano(1)
                    break
        else:
            barra.fill('green')
        barra_fundo.blit(barra, (tamanho_maximo - tempo_restante * escala + margem, margem))
        self.__tela.blit(barra_fundo, (max(0, self.__configuracoes.largura_tela - tamanho_maximo - 20), 100))

    def adicionar_tempo(self, tempo: int):
        self.__tempo_maximo += tempo
        self.__tempo_maximo = min(self.__tempo_maximo, 60 + self.__tempo.ver_tempo())

    def jogo_perdido(self):
        tempo = self.__tempo.ver_tempo()
        self.__armazenamento.adicionar_pontuacao(self.__armazenamento.nome_da_partida, tempo, self.__fase_atual_indice)
        self.__armazenamento.apagar_partida()
        self._maquina_de_estado.mover_para_estado('fim_de_jogo')
        self.__tem_jogo = False

    def __gerar_estado(self) -> dict:
        jogador = self.__jogador.gerar_dict_do_estado()
        return {
            'tempo_restante': self.__tempo_maximo - self.__tempo.ver_tempo(),
            'tempo': self.__tempo.ver_tempo(),
            'indice_fase': self.__fase_atual_indice,
            'jogador': jogador
        }

    def iniciar_fase(self):
        self.__fases[self.__fase_atual_indice].iniciar(jogador=self.__jogador)
        self.__armazenamento.salvar_partida(self.__gerar_estado())

    def terminar_fase(self):
        self.__ultimo_quadro_fase = self.__tela.copy()
        self.__fase_ativa = False
        self.__callback_de_eventos = []

    def desenhar(self):
        self.__tela.fill('black')
        if self.__fase_ativa:
            self.__tela.blit(self.__fases[self.__fase_atual_indice].desenhar(), (0, 0))
            if not self.__transicao.terminou:
                self.__tela.blit(self.__transicao.desenhar(), (0, 0))
        else:
            if self.__ultimo_quadro_fase is not None:
                self.__tela.blit(self.__ultimo_quadro_fase, (0, 0))
                self.__tela.blit(self.__transicao.desenhar(), (0, 0))
        self.__desenhar_barra_tempo()
        self.__desenhar_tempo()

    def atualizar(self, eventos: List[pg.event.Event], tempo_passado: int):
        if self.__fase_ativa:
            self.__atualizar_fase(eventos, tempo_passado)
            if not self.__transicao.terminou:
                self.__transicao.atualizar(tempo_passado)
        else:
            self.__transicao.atualizar(tempo_passado)
            if self.__transicao.iniciou:
                self.__fase_atual_indice += 1
                self.__fase_ativa = True
                if self.__fase_atual_indice >= len(self.__fases):
                    self.__armazenamento.adicionar_pontuacao(
                        self.__armazenamento.nome_da_partida,
                        self.__tempo.ver_tempo(),
                        self.__fase_atual_indice
                    )
                    self.__armazenamento.apagar_partida()
                    self._maquina_de_estado.mover_para_estado('menu_vitoria')
                    self.__tem_jogo = False
                else:
                    self.iniciar_fase()

    def __atualizar_fase(self, eventos: List[pg.event.Event], tempo_passado: int):
        self.__fases[self.__fase_atual_indice].atualizar(tempo_passado)
        if len(self.__callback_eventos_de_tempo) > 0:
            self.__marcador_de_tempo_para_eventos += tempo_passado
        else:
            self.__marcador_de_tempo_para_eventos = 0
        i = len(self.__callback_eventos_de_tempo) - 1
        while i >= 0:
            identifier, tempo, callback = self.__callback_eventos_de_tempo[i]
            if tempo <= self.__marcador_de_tempo_para_eventos:
                callback()
                self.__callback_eventos_de_tempo.pop(i)
            i -= 1
        for evento in eventos:
            if evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                self._maquina_de_estado.mover_para_estado('menu_pausa')
                self.__tempo.pausar()
            else:
                for callback_de_evento in self.__callback_de_eventos:
                    if evento.type == callback_de_evento.tipo:
                        callback_de_evento.disparar(evento)

    def iniciar(self):
        if not self.__tem_jogo:
            self.__fase_atual_indice = 0
            self.__tem_jogo = True
            self.__tempo = Tempo()
            self.__tempo.iniciar()
            estado = self.__armazenamento.partida
            if estado:
                self.__fase_atual_indice = estado['indice_fase']
                self.__tempo.retomar(estado['tempo'])
                self.__tempo_maximo = estado['tempo_restante'] + estado['tempo']
                self.__jogador = Jogador(**estado['jogador'])
            else:
                self.__jogador = Jogador()
            self.iniciar_fase()
        else:
            self.__tempo.retomar()
        self.__musica_control.parar_musica()
        self.__musica_control.iniciar_musica(self.__configuracoes.musica_jogo)
