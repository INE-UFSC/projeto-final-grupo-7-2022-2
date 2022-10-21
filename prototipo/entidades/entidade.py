from abc import ABC

class Entidade(ABC):
    def registrar_na_fase(self, fase: Fase):
        raise NotImplementedError("Registrar na fase não implementado")

    @property
    def tipo(self):
        raise NotImplementedError("Tipo não implementado")

    def atualizar(self, delta: float):
        raise NotImplementedError("Atualizar não implementado")

    def renderizar(self, tela: pygame.Surface):
        raise NotImplementedError("Renderizar não implementado")

    def receber_dano(self, dano: int):
        raise NotImplementedError("Receber dano não implementado")
