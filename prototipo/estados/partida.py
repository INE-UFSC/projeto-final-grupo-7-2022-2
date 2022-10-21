from fase import Fase


class Partida:

    def __init__(self):
        raise NotImplementedError("Partida não implementada")

    def registrar_evento(self, tipo: str, callback: Callable) -> int:
        raise NotImplementedError("Registrar evento não implementado")

    def remover_registro_de_evento(self, id: int):
        raise NotImplementedError("Remover registro de evento não implementado")

    def registrar_fase(self, fase: Fase):
        raise NotImplementedError("Registrar fase não implementado")

    def terminar_fase(self):
        raise NotImplementedError("Terminar fase não implementado")
