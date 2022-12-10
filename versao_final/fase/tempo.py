import time


class Tempo:
    def __init__(self):
        self.__tempo_inicio = None
        self.__tempo_pausado = None
        self.__pausado = False

    def zerar(self):
        self.__tempo_inicio = None
        self.__tempo_pausado = None
        self.__pausado = False

    def iniciar(self):
        self.zerar()
        self.__tempo_inicio = time.time()

    def pausar(self):
        self.__tempo_pausado = time.time()
        self.__pausado = True

    def retomar(self):
        if self.__tempo_inicio is not None and self.__pausado:
            momento_pause = time.time() - self.__tempo_pausado
            self.__tempo_inicio = self.__tempo_inicio + momento_pause
            self.__pausado = False

    def ver_tempo(self):
        if self.__pausado:
            return self.__tempo_pausado - self.__tempo_inicio
        else:
            return time.time() - self.__tempo_inicio

    def temporizador(self, tempo_maximo):
        tempo_fim = int(tempo_maximo - self.__tempo_inicio)
        return tempo_maximo - self.ver_tempo()