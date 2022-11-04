class Botao:

    def __init__(self):
        raise NoneImplementedError("Botão não implementado")

    def atualizar(self, status: str):
        raise NoneImplementedError("Atualizar não implementado")

    def on_click(self):
        raise NoneImplementedError("On click não implementado")

    def desenhar(self):
        raise NoneImplementedError("Desenhar não implementado")
