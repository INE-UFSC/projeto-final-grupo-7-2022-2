from callback_de_evento import CallbackDeEvento


class Partida:

    def __init__(self, jogo):
        self.__fases = []
        self.__fase_atual_indice = 0
        self.__callback_de_eventos = []
        self.__id_indice = 0
        self.__jogo = jogo

    def registrar_evento(self, tipo: int, callback: callable) -> int:
        id = self.__id_indice
        callback_de_evento = CallbackDeEvento(id, tipo, callback)
        self.__callback_de_eventos.append(callback_de_evento)
        self.__id_indice += 1
        return id

    def remover_registro_de_evento(self, id: int):
        for callback_de_evento in self.__callback_de_eventos:
            if callback_de_evento.id == id:
                self.__callback_de_eventos.remove(callback_de_evento)
                break

    def registrar_fase(self, fase: 'Fase'):
        self.__fases.append(fase)

    def terminar_fase(self):
        self.__fase_atual_indice += 1
        if self.__fase_atual_indice >= len(self.__fases):
            self.__jogo().mover_para_estado('fim_de_jogo')

    def desenhar(self):
        self.__fases[self.__fase_atual_indice].desenhar()

    def atualizar(self, eventos: list, delta_time: float):
        self.__fases[self.__fase_atual_indice].atualizar(delta_time)
        for evento in eventos:
            for callback_de_evento in self.__callback_de_eventos:
                if evento.type == callback_de_evento.tipo:
                    callback_de_evento.disparar(evento)
