import json

from .singleton import Singleton


class Armazenamento(Singleton):
    def __init__(self):
        self.__nome_do_arquivo = 'estado.json'
        self.__ler_arquivo()

    def __ler_arquivo(self):
        try:
            with open(self.__nome_do_arquivo, 'r', encoding='utf-8') as file:
                self.__conteudo = json.load(file)
        except FileNotFoundError:
            self.__conteudo = {}
            self.__salvar_arquivo()

    def __salvar_arquivo(self):
        with open(self.__nome_do_arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.__conteudo, f, ensure_ascii=False, indent=4)

    @property
    def volume_musica(self):
        return self.__conteudo.get('volume_musica', 1)

    @property
    def ultima_pontuacao(self):
        return self.__ultima_pontuacao

    @property
    def volume_som(self):
        return self.__conteudo.get('volume_som', 1)

    @volume_musica.setter
    def volume_musica(self, valor: int):
        self.__conteudo['volume_musica'] = valor
        self.__salvar_arquivo()

    @volume_som.setter
    def volume_som(self, valor: int):
        self.__conteudo['volume_som'] = valor
        self.__salvar_arquivo()

    def adicionar_pontuacao(self, nome: str, tempo: int, fase_indice: int):
        self.__conteudo['pontuacao'] = self.__conteudo.get('pontuacao', [])
        potuacao = {'nome': nome, 'tempo': tempo, 'fase_indice': fase_indice}
        self.__ultima_pontuacao = potuacao
        self.__conteudo['pontuacao'].append(potuacao)
        self.__conteudo['pontuacao'].sort(key=lambda x: x['tempo'])
        self.__conteudo['pontuacao'].sort(key=lambda x: -x['fase_indice'])
        self.__salvar_arquivo()

    @property
    def pontuacoes(self):
        return self.__conteudo.get('pontuacao', [])

    @property
    def nome_da_partida(self) -> str | None:
        return self.__conteudo.get('nome_da_partida', None)

    @nome_da_partida.setter
    def nome_da_partida(self, nome: str):
        self.__conteudo['nome_da_partida'] = nome
        self.__salvar_arquivo()

    def salvar_partida(self, dict):
        self.__conteudo['partida'] = dict
        self.__salvar_arquivo()

    def apagar_partida(self):
        del self.__conteudo['partida']
        del self.__conteudo['nome_da_partida']
        self.__salvar_arquivo()

    @property
    def partida(self) -> dict | None:
        return self.__conteudo.get('partida', None)
