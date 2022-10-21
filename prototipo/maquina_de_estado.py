
class MaquinaDeEstado:
    def __init__(self):
        self.__estados_dicts = {}
        self.__estado_atual = None
        self.__estado_incial = None
        raise NotImplementedError("Maquina de estado não implementada")

    @property
    def estado_inicio(self):
        return self.__estado_inicial

    @estado_inicio.setter
    def estado_inicio(self, estado_inicio):
        self.__estado_inicial = estado_inicio

    def adicionar_estado(self, rotulo: str, estado: 'Estado'):
        raise NotImplementedError("Adicionar estado não implementado")

    def iniciar(self):
        raise NotImplementedError("Iniciar não implementado")
