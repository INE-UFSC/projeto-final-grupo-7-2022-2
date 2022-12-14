class Configuracoes:
    def __init__(self):
        self.__altura_tela = 720
        self.__largura_tela = 1280 
        self.__tamanho_tile = 32
        self.__volume_musica = 0
        self.__max_fps = 240
        self.__tps = 60

    @property
    def tps(self):
        return self.__tps

    @property
    def max_fps(self):
        return self.__max_fps

    @property
    def tamanho_tile(self):
        return self.__tamanho_tile

    @property
    def largura_tela(self):
        return self.__largura_tela

    @largura_tela.setter
    def largura_tela(self, largura_tela):
        self.__largura_tela = largura_tela

    @property
    def altura_tela(self):
        return self.__altura_tela

    @altura_tela.setter
    def altura_tela(self, altura_tela):
        self.__altura_tela = altura_tela

    @property
    def volume_musica(self):
        return self.__volume_musica

    @volume_musica.setter
    def volume_musica(self, volume_musica):
        self.__volume_musica = volume_musica
