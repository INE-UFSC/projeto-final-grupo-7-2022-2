import os
from typing import TYPE_CHECKING, List

import pygame as pg
import pytmx

from entidades import Arqueiro, BombaDeAsma, Entidade, Guerreiro, Ladino
from utilidades import Configuracoes
from visualizacao import SuperficiePosicionada, Tile

if TYPE_CHECKING:
    from fase import Fase
class CamadaNaoEncontrada(Exception):
    pass

class GerenciadorDeGrupos():
    def __init__(self, fase: 'Fase', nome: str):

        self.__configuracao = Configuracoes()
        self.__fase = fase
        self.__nome = nome

        # Carrega o arquivo .tmx
        tmx_path = os.path.join('./visualizacao/mapas', self.__nome, self.__nome + '.tmx')
        dados_do_pytmx = pytmx.load_pygame(tmx_path, pixelalpha=True)
        self.__chao = self.__gerar_chao(dados_do_pytmx)
        self.__blocos_superiores = self.__gerar_superficie_unica_da_camada(dados_do_pytmx, 'blocos_superiores')
        self.__gerar_camada_intermediaria(dados_do_pytmx)
        self.__gerar_colisores(dados_do_pytmx)
        self.__gerar_entidades(dados_do_pytmx)

    # Camada inferior:
    @property
    def chao(self) -> SuperficiePosicionada:
        return self.__chao

    @property
    def blocos_estaticos(self) -> List[Tile]:
        return self.__blocos_estaticos

    @property
    def blocos_dinamicos(self) -> List[Tile]:
        return self.__blocos_dinamicos

    # Camada superior:
    @property
    def blocos_superiores(self) -> SuperficiePosicionada:
        return self.__blocos_superiores

    # Outros:
    @property
    def entidades(self) -> List[Entidade]:
        return self.__entidades

    @property
    def colisores(self) -> List[Tile]:
        return self.__colisores

    def __gerar_chao(self, dados: pytmx.TiledMap) -> SuperficiePosicionada:
        chao = self.__gerar_superficie_unica_da_camada(dados, 'chao')
        try:
            chao_detalhes = self.__gerar_superficie_unica_da_camada(dados, 'chao_detalhes')
            chao.superficie.blit(chao_detalhes.superficie, chao_detalhes.posicao)
        except CamadaNaoEncontrada:
            pass
        
        return chao

    def __gerar_superficie_unica_da_camada(self, dados: pytmx.TiledMap, camada: str) -> None:
        for layer in dados.visible_layers:
            if hasattr(layer, 'data'):
                tamanho_tile = self.__configuracao.tamanho_tile
                superficie_final = pg.Surface((tamanho_tile * layer.width, tamanho_tile * layer.height))
                superficie_final.set_colorkey((0, 0, 0))
                print(layer.name, camada)
                if layer.name == camada:
                    for x, y, superficie_da_tile in layer.tiles():
                        x = x * self.__configuracao.tamanho_tile
                        y = y * self.__configuracao.tamanho_tile
                        w = self.__configuracao.tamanho_tile
                        h = self.__configuracao.tamanho_tile
                        superficie_escalada = pg.transform.scale(superficie_da_tile, (w, h))
                        superficie_final.blit(superficie_escalada, (x, y), (0, 0, w, h))
                    
                    return SuperficiePosicionada(superficie=superficie_final, topo_esquerdo=(0, 0))

        raise CamadaNaoEncontrada(f'Não foi possível encontrar a camada "{camada}" no arquivo .tmx')

    def __gerar_camada_intermediaria(self, dados: pytmx.TiledMap) -> None:

        # Cria uma lista com os blocos que seguem o grid do mapa
        # Nenhum desses blocos é interativo
        # Podem ser paredes, grades, etc
        blocos_estaticos = []
        for layer in dados.visible_layers:
            if hasattr(layer, 'data'):
                if layer.name == 'blocos':
                    for x, y, superficie in layer.tiles():
                        posicao = (x * self.__configuracao.tamanho_tile, y * self.__configuracao.tamanho_tile)
                        blocos_estaticos.append(Tile(posicao=posicao, superficie=superficie))

        # Cria uma lista com objetos que não seguem o grid do mapa, mas não tem interação com a fase
        # Podem ser árvores, estátuas, pedras, etc
        for grupo in dados.objectgroups:
            if grupo.name == 'objetos_estaticos':
                for objeto in grupo:
                    superficie = pg.Surface(size=(objeto.width, objeto.height))
                    posicao = objeto.x, objeto.y
                    blocos_estaticos.append(
                        Tile(
                            posicao,
                            superficie=superficie,
                            largura=objeto.width,
                            altura=objeto.height))

        self.__blocos_estaticos = blocos_estaticos
        # Cria uma lista com objetos que não seguem o grid do mapa, mas tem interação com a fase
        # Podem ser portas, armadilhas, etc
        blocos_dinamicos = []
        for grupo in dados.objectgroups:
            if grupo.name == 'objetos_dinamicos':
                for estrutura in grupo:
                    posicao = estrutura.x, estrutura.y
                    blocos_dinamicos.append(
                        Tile(
                            posicao,
                            superficie=superficie,
                            largura=objeto.width,
                            altura=objeto.height))

        self.__blocos_dinamicos = blocos_dinamicos

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
