import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.object_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.object_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # Obtener la columna de la textura
            wall_column = self.textures[str(texture)].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)

            # Escalar la columna según la proyección calculada
            wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)

            # Agregar el objeto renderizable a la lista
            self.object_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        EPSILON = 0.000001  # Para evitar divisiones por cero
        for ray in range(NUM_RAYS):
            # Asegurar que sin_a y cos_a no sean cercanos a 0
            sin_a = math.sin(ray_angle) if abs(math.sin(ray_angle)) > EPSILON else EPSILON
            cos_a = math.cos(ray_angle) if abs(math.cos(ray_angle)) > EPSILON else EPSILON

            # Cálculo de intersecciones horizontales
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth_hor = dy / sin_a
            dx_hor = delta_depth_hor * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx_hor
                y_hor += dy
                depth_hor += delta_depth_hor

            # Cálculo de intersecciones verticales
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth_vert = dx / cos_a
            dy_vert = delta_depth_vert * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy_vert
                depth_vert += delta_depth_vert

            # Determinación de la profundidad y textura
            if depth_hor < depth_vert:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = x_hor if sin_a > 0 else 1 - x_hor
            else:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else 1 - y_vert

            # Corrección del efecto "fish-eye"
            corrected_depth = depth * math.cos(self.game.player.angle - ray_angle)

            # Cálculo de la altura proyectada del muro
            proj_height = int(SCREEN_DIST / (corrected_depth + 0.0001))  # Evitar divisiones por cero

            # Guardar los resultados del ray casting
            self.ray_casting_result.append((corrected_depth, proj_height, texture, offset))

            # Incrementar el ángulo del rayo para el siguiente
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
