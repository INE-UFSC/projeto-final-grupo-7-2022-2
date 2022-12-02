import os
from typing import TYPE_CHECKING, List

import pygame as pg
import pytmx

from configuracoes import Configuracoes
from entidades import Arqueiro, Entidade, Guerreiro, Ladino

from View.tile import Tile

if TYPE_CHECKING:
    from fase import Fase


class GerenciadorDeGrupos():
    def __init__(self, fase: 'Fase', nome: str):

        self.__configuracao = Configuracoes()
        self.__fase = fase
        self.__nome = nome

        # Carrega o arquivo .tmx
        tmx_path = os.path.join('./View/mapas', self.__nome, self.__nome + '.tmx')
        dados_do_pytmx = pytmx.load_pygame(tmx_path, pixelalpha=True)
        self.__gerar_blocos(dados_do_pytmx)
        self.__gerar_colisores(dados_do_pytmx)
        self.__gerar_chao(dados_do_pytmx)
        self.__gerar_estruturas(dados_do_pytmx)
        self.__gerar_entidades(dados_do_pytmx)

    @property
    def chao(self) -> pg.surface.Surface:
        return self.__chao

    @property
    def entidades(self) -> List[Entidade]:
        return self.__entidades

    @property
    def blocos(self) -> List[Tile]:
        return self.__blocos

    @property
    def colisores(self) -> List[Tile]:
        return self.__colisores

    @property
    def estruturas(self) -> List[Tile]:
        return self.__estruturas

    def __gerar_chao(self, dados: pytmx.TiledMap) -> None:
        floor_path = os.path.join('./View/mapas', self.__nome, 'floor.png')
        superficie = pg.image.load(floor_path).convert_alpha()
        altura = dados.height * self.__configuracao.tamanho_tile
        largura = dados.width * self.__configuracao.tamanho_tile

        self.__chao = pg.transform.scale(superficie, (largura, altura))

    def __gerar_blocos(self, dados: pytmx.TiledMap) -> None:

        blocos = []
        for layer in dados.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, superficie in layer.tiles():
                    posicao = (x * self.__configuracao.tamanho_tile, y * self.__configuracao.tamanho_tile)
                    blocos.append(Tile(posicao=posicao, superficie=superficie))

        self.__blocos = blocos

    def __gerar_colisores(self, dados: pytmx.TiledMap) -> None:

        colisores = []
        for layer in dados.layers:
            if hasattr(layer, 'data'):
                if layer.name == 'collision' or layer.name == 'object_obstacles':
                    for x, y, superficie in layer.tiles():
                        posicao = (x * self.__configuracao.tamanho_tile, y * self.__configuracao.tamanho_tile)
                        colisores.append(Tile(posicao=posicao, superficie=superficie))

        self.__colisores = colisores

    def __gerar_estruturas(self, dados: pytmx.TiledMap) -> None:

        estruturas = []
        # Percorre o arquivo tmx e inlcui os objetos em seu respectivo grupo
        for grupo in dados.objectgroups:
            if grupo.name == 'structures':
                for estrutura in grupo:
                    posicao = estrutura.x, estrutura.y
                    estruturas.append(
                        Tile(
                            posicao,
                            superficie=estrutura.image,
                            largura=estrutura.width,
                            altura=estrutura.height))

        self.__estruturas = estruturas

    def __gerar_entidades(self, dados: pytmx.TiledMap) -> None:
        entidades: List[Entidade] = []
        for grupo in dados.objectgroups:
            if grupo.name == 'entities':
                for entidade in grupo:
                    if entidade.name == 'player':
                        entidades.append(self.__fase.jogador)
                        self.__fase.jogador.definir_posicao(pg.Vector2(entidade.x, entidade.y))
                    elif entidade.name == 'ladino':
                        ladino = Ladino()
                        ladino.definir_posicao(posicao=pg.Vector2(entidade.x, entidade.y))
                        entidades.append(ladino)
                    elif entidade.name == 'guerreiro':
                        guerreiro = Guerreiro()
                        guerreiro.definir_posicao(posicao=pg.Vector2(entidade.x, entidade.y))
                        entidades.append(guerreiro)
                    elif entidade.name == 'arqueiro':
                        arqueiro = Arqueiro()
                        arqueiro.definir_posicao(posicao=pg.Vector2(entidade.x, entidade.y))
                        entidades.append(arqueiro)

        self.__entidades = entidades

    def matar_entidade(self, entidade: Entidade) -> None:
        self.__entidades.remove(entidade)
