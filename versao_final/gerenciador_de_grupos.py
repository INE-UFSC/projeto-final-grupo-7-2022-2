import os
from typing import TYPE_CHECKING, List

import pygame as pg
import pytmx

from configuracoes import Configuracoes
from entidades import Arqueiro, Entidade, Guerreiro, Ladino, BombaDeAsma

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
        self.__gerar_camada_superior(dados_do_pytmx)
        self.__gerar_estruturas(dados_do_pytmx)
        self.__gerar_entidades(dados_do_pytmx)

    @property
    def chao(self) -> list[Tile]:
        return self.__chao

    @property
    def camada_superior(self) -> list[Tile]:
        return self.__camada_superior

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

        chao = []
        for layer in dados.visible_layers:
            if hasattr(layer, 'data'):
                if layer.name == 'chao':
                    for x, y, superficie in layer.tiles():
                        posicao = (x * self.__configuracao.tamanho_tile, y * self.__configuracao.tamanho_tile)
                        chao.append(Tile(posicao=posicao, superficie=superficie))

        self.__chao = chao

    def __gerar_camada_superior(self, dados: pytmx.TiledMap) -> None:
        
        camada_superior = []
        for layer in dados.visible_layers:
            if hasattr(layer, 'data'):
                if layer.name == 'camada_superior':
                    for x, y, superficie in layer.tiles():
                        posicao = (x * self.__configuracao.tamanho_tile, y * self.__configuracao.tamanho_tile)
                        camada_superior.append(Tile(posicao=posicao, superficie=superficie))

        self.__camada_superior = camada_superior

    def __gerar_blocos(self, dados: pytmx.TiledMap) -> None:

        blocos = []
        for layer in dados.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, superficie in layer.tiles():
                    posicao = (x * self.__configuracao.tamanho_tile, y * self.__configuracao.tamanho_tile)
                    blocos.append(Tile(posicao=posicao, superficie=superficie))

        self.__blocos = blocos

    def __unir_tiles_proximas(self, tiles: List[Tile]) -> List[Tile]:
        novas_tiles_por_y = {}
        for tile in tiles:
            if tile.rect.y not in novas_tiles_por_y:
                novas_tiles_por_y[tile.rect.y] = [tile]
            else:
                novas_tiles_por_y[tile.rect.y].append(tile)

        for novas_tiles in novas_tiles_por_y.values():
            novas_tiles.sort(key=lambda tile: tile.rect.x)
            i = 0
            while i < len(novas_tiles) - 1:
                if novas_tiles[i].rect.x + novas_tiles[i].rect.width == novas_tiles[i + 1].rect.x and \
                        novas_tiles[i].rect.height == novas_tiles[i + 1].rect.height:
                    x = novas_tiles[i].rect.x
                    y = novas_tiles[i].rect.y
                    largura = novas_tiles[i].rect.width + novas_tiles[i + 1].rect.width
                    altura = novas_tiles[i].rect.height
                    superficie = novas_tiles[i].superficie
                    tile = Tile((x, y), superficie=superficie,  largura=largura, altura=altura)
                    novas_tiles[i] = tile
                    del novas_tiles[i + 1]
                else:
                    i += 1
        novas_tiles_por_x = {}
        for novas_tiles in novas_tiles_por_y.values():
            for tile in novas_tiles:
                if tile.rect.x not in novas_tiles_por_x:
                    novas_tiles_por_x[tile.rect.x] = [tile]
                else:
                    novas_tiles_por_x[tile.rect.x].append(tile)

        for novas_tiles in novas_tiles_por_x.values():
            novas_tiles.sort(key=lambda tile: tile.rect.y)
            i = 0
            while i < len(novas_tiles) - 1:
                if novas_tiles[i].rect.y + novas_tiles[i].rect.height == novas_tiles[i + 1].rect.y and \
                        novas_tiles[i].rect.width == novas_tiles[i + 1].rect.width:
                    x = novas_tiles[i].rect.x
                    y = novas_tiles[i].rect.y
                    largura = novas_tiles[i].rect.width
                    altura = novas_tiles[i].rect.height + novas_tiles[i + 1].rect.height
                    superficie = novas_tiles[i].superficie
                    tile = Tile((x, y), superficie=superficie,  largura=largura, altura=altura)
                    novas_tiles[i] = tile
                    del novas_tiles[i + 1]
                else:
                    i += 1
        return [tile for novas_tiles in novas_tiles_por_x.values() for tile in novas_tiles]

    def __gerar_colisores(self, dados: pytmx.TiledMap) -> None:

        colisores = []

        for grupo in dados.objectgroups:
            if grupo.name == 'objetos_de_colisao':
                for estrutura in grupo:
                    superficie = pg.Surface((estrutura.width, estrutura.height))
                    superficie.fill('white')
                    superficie.set_alpha(128)
                    posicao = estrutura.x, estrutura.y
                    colisores.append(
                        Tile(
                            posicao,
                            superficie=superficie,
                            largura=estrutura.width,
                            altura=estrutura.height))

        self.__colisores = self.__unir_tiles_proximas(colisores)

    def __gerar_estruturas(self, dados: pytmx.TiledMap) -> None:

        estruturas = []

        # Percorre o arquivo tmx e inlcui os objetos em seu respectivo grupo
        for grupo in dados.objectgroups:
            if grupo.name == 'estruturas':
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
        bomba_de_asma = BombaDeAsma()
        entidades: List[Entidade] = [bomba_de_asma]
        if dados.tilewidth != dados.tileheight:
            raise ValueError('Mapa com tiles de largura e altura diferentes')
        escala = self.__configuracao.tamanho_tile / dados.tilewidth
        bomba_de_asma.definir_posicao(pg.Vector2(30, 40) * escala)

        for grupo in dados.objectgroups:
            if grupo.name == 'entidades':
                for entidade in grupo:
                    if entidade.name == 'jogador':
                        entidades.append(self.__fase.jogador)
                        self.__fase.jogador.definir_posicao(pg.Vector2(entidade.x, entidade.y) * escala)
                    elif entidade.name == 'ladino':
                        ladino = Ladino()
                        ladino.definir_posicao(posicao=pg.Vector2(entidade.x, entidade.y) * escala)
                        entidades.append(ladino)
                    elif entidade.name == 'guerreiro':
                        guerreiro = Guerreiro()
                        guerreiro.definir_posicao(posicao=pg.Vector2(entidade.x, entidade.y) * escala)
                        entidades.append(guerreiro)
                    elif entidade.name == 'arqueiro':
                        arqueiro = Arqueiro()
                        arqueiro.definir_posicao(posicao=pg.Vector2(entidade.x, entidade.y) * escala)
                        entidades.append(arqueiro)

        self.__entidades = entidades

    def matar_entidade(self, entidade: Entidade) -> None:
        self.__entidades.remove(entidade)
