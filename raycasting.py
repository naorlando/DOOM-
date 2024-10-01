import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        EPSILON = 0.000001  
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
                    break
                x_vert += dx
                y_vert += dy_vert
                depth_vert += delta_depth_vert

            # Seleccionar la menor profundidad entre horizontal y vertical
            depth = min(depth_hor, depth_vert)

            # "fish-eye effect"
            corrected_depth = depth * math.cos(self.game.player.angle - ray_angle)

            #
            pg.draw.line(self.game.screen, 'yellow',
                         (100 * ox, 100 * oy),
                         (100 * ox + 100 * corrected_depth * cos_a, 100 * oy + 100 * corrected_depth * sin_a), 2)

            # Incrementar el ángulo del rayo
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
