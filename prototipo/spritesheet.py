class Spritesheet:
    def __init__(self, caminho_da_imagem: str, largura: int, altura: int):
        raise NotImplementedError("Spritesheet não implementado")

    def get_sprite(self, linha: int, coluna: int) -> pygame.Surface:
        raise NotImplementedError("Get sprite não implementado")
