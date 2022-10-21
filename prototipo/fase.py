class Fase:
    def __init__(self):
        raise NotImplementedError("Fase não implementada")

    def registrar_evento(self, tipo, callback: callable):
        raise NotImplementedError("Registrar evento não implementado")

    def terminar_fase(self):
        raise NotImplementedError("Terminar fase não implementado")
