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

    def adicionar_pontuacao(self, nome: str, pontuacao: int):
        self.__conteudo['pontuacao'] = self.__conteudo.get('pontuacao', [])
        self.__conteudo['pontuacao'].append({'nome': nome, 'pontuacao': pontuacao})
        self.__salvar_arquivo()

    def salvar_partida(self, dict):
        self.__conteudo['partida'] = dict
        self.__salvar_arquivo()

    def apagar_partida(self):
        self.__conteudo['partida'] = {}
        self.__salvar_arquivo()

    @property
    def partida(self) -> dict | None:
        return self.__conteudo.get('partida', None)
