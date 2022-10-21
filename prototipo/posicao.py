class Posicao:

    def __init__(self, x: int, y: int, largura: int, altura: int):
        raise NotImplementedError("Posicao não implementado")

    def copy(self):
        raise NotImplementedError("Copy não implementado")

    def esta_sobrepondo(self, outro: Posicao) -> bool:
        raise NotImplementedError("Esta sobrepondo não implementado")
