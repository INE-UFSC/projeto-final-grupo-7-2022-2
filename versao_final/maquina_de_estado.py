class MaquinaDeEstado:
    def __init__(self):
        self.__estados = {}
        self.__estado_pilha = []
        self.__estado_atual: Estado | None = None
        self.__estado_inicial: Estado | None = None

    @property
    def estado_inicial(self):
        return self.__estado_inicial

    @property
    def estado_atual(self):
        return self.__estado_atual

    @estado_inicial.setter
    def estado_inicial(self, estado_inicial):
        self.__estado_inicial = estado_inicial

    def adicionar_estado(self, rotulo: str, estado: 'Estado'):
        self.__estados[rotulo] = estado
        if len(self.__estados) == 1 and self.__estado_inicial is None:
            self.__estado_inicial = rotulo

    def mover_para_estado(self, rotulo: str):
        self.__estado_pilha.append(self.__estado_atual)
        self.__estado_atual = self.__estados[rotulo]
        

    def voltar_para_inicio(self):
        self.__estado_atual = self.__estado_inicial
        self.__estado_pilha = []
        
    def voltar(self):
        ultimo_estado = self.__estado_pilha.pop()
        if ultimo_estado is not None:
            self.__estado_atual = ultimo_estado
        else: 
            self.voltar_para_inicio()
    
    def iniciar(self):
        pass