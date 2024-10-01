import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.wall_textures = self.load_wall_textures()

    def draw(self):
        self.render_game_objects()

    def render_game_objects(self):
        # Ordenamos los objetos por profundidad (de mayor a menor)
        list_objects = sorted(self.game.raycasting.object_to_render, key=lambda obj: obj[0], reverse=True)
        
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        try:
            texture = pg.image.load(path).convert_alpha()
            return pg.transform.scale(texture, res)
        except FileNotFoundError:
            print(f"Error: La textura en {path} no se pudo cargar.")
            return pg.Surface(res)  # Devuelve una superficie vacía como fallback

    def load_wall_textures(self):
        textures = {}
        texture_paths = {
            '1': 'textures/1.png',
            '2': 'textures/2.png',
            '3': 'textures/3.png',
            '4': 'textures/4.png',
            '5': 'textures/5.png'
        }

        for key, path in texture_paths.items():
            textures[key] = self.get_texture(path)

        return textures
