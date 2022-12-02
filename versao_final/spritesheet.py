import pygame as pg
import os
import json


class Spritesheet():
    def __init__(self, sheet_name: str, scale=1) -> None:
        # Carrega a sprite sheet como uma surface
        self.__scale = scale
        sheet_surf = pg.image.load(os.path.join('recursos', 'sprites', sheet_name + '.png')).convert_alpha()
        self.__sheet = pg.transform.scale(sheet_surf, (sheet_surf.get_width() * scale, sheet_surf.get_height() * scale))

        # Abre o arquivo json da spritesheet,carrega ele como um dicionário e armazena esse dicionário em self.__data
        with open(os.path.join('recursos', 'sprites', sheet_name + '.json'), 'r') as f:
            self.__data = json.load(f)

    def get_sprite(self, sprite_name: str) -> pg.Surface:
        # Atalhos para dados da spritesheet:
        sprite_data = self.__data["frames"][sprite_name]["frame"]
        x, y, w, h = sprite_data["x"] * self.__scale, sprite_data["y"] * \
            self.__scale, sprite_data["w"] * self.__scale, sprite_data["h"] * self.__scale

        sprite = pg.Surface((w, h))  # Cria a superfície da sprite, de largura w e altura h
        sprite.set_colorkey((0, 0, 0))  # Define a cor chave para utilizar transparência como preto (0,0,0)

        sprite.blit(self.__sheet, (0, 0), (x, y, w, h))  # Cola o recorte da spritesheet na superfície da sprite

        return sprite

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

        for spr in spr_list:
            spr = spr
            spr_info = spr.split("_")  # Separa o nome da sprite em um estado e um passo e coloca eles numa lista.
            state = spr_info[0]  # Indica o estado da animação (idle, run, hit, etc)
            step = self.get_sprite(spr)  # Indica o passo da animação (0, 1, 2, ...)

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
