import pygame as pg
import os
import json
from configuracoes import Configuracoes


class Spritesheet():
    def __init__(self, sheet_name: str) -> None:
        # Carrega a sprite sheet como uma surface
        self.__configuracoes = Configuracoes()
        self.__sheet = pg.image.load(os.path.join('recursos', 'sprites', sheet_name + '.png')).convert_alpha()
        # Abre o arquivo json da spritesheet,carrega ele como um dicionário e armazena esse dicionário em self.__data
        with open(os.path.join('recursos', 'sprites', sheet_name + '.json'), 'r') as f:
            self.__data = json.load(f)

    def get_sprite(self, sprite_name: str, escala: float) -> pg.Surface:
        # Atalhos para dados da spritesheet:
        sprite_data = self.__data["frames"][sprite_name]["frame"]

        x = sprite_data["x"]
        y = sprite_data["y"]
        w = sprite_data["w"]
        h = sprite_data["h"]

        sprite = pg.Surface((w, h))  # Cria a superfície da sprite, de largura w e altura h
        sprite.set_colorkey((0, 0, 0))  # Define a cor chave para utilizar transparência como preto (0,0,0)

        sprite.blit(self.__sheet, (0, 0), (x, y, w, h))  # Cola o recorte da spritesheet na superfície da sprite
        return pg.transform.scale(sprite, (int(w * escala), int(h * escala)))  # Redimensiona a sprite para o tamanho do tile
         

    @property
    def sprite_list(self) -> list:
        return self.__data["frames"].keys()

    def get_animation_frames(self) -> dict:
        animation_dict = {
            'right': [],
            'left': [],
            'right_idle': [],
            'left_idle': []
        }
        spr_list = self.sprite_list
        escala = None
        for spr in spr_list:
            escala_nova = self.__configuracoes.tamanho_tile / self.__data["frames"][spr]["sourceSize"]["w"]
            if escala is None:
                escala = escala_nova
            elif escala != escala_nova:
                raise ValueError("Tamanho de tile incompatível com a spritesheet.")

            spr_info = spr.split("_")  # Separa o nome da sprite em um estado e um passo e coloca eles numa lista.
            state = spr_info[0]  # Indica o estado da animação (idle, run, hit, etc)
            step = self.get_sprite(spr, escala)  # Indica o passo da animação (0, 1, 2, ...)

            if 'run' in state:
                animation_dict['right'].append(step)
                animation_dict['left'].append(pg.transform.flip(step, True, False))
            elif 'idle' in state:
                animation_dict['right_idle'].append(step)
                animation_dict['left_idle'].append(pg.transform.flip(step, True, False))

        return animation_dict


'''
For better reference of what is happening above, check the spritesheet's JSON file structure.
'''
