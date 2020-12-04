import numpy as np

# Local Modules
from constants import BOX_SIZE, COLOR_CHANNELS, MAX_VALUE
from particle import Shape

HEIGHT = 720
WIDTH = 1280


def draw_rectangle(x0, y0, x1, y1, img_arr, color):
    x0 = int(round(x0))
    y0 = int(round(y0))
    x1 = int(round(x1))
    y1 = int(round(y1))
    for j in range(y1, y0):
        for i in range(x0, x1):
            img_arr[j][i] = color


def render(particles, h=HEIGHT, w=WIDTH):
    img_arr = np.zeros([h, w, COLOR_CHANNELS], dtype=np.uint8)
    for particle in particles:
        center = particle.get_position()
        if particle.shape == Shape.BOX:
            x0 = center[0] - (BOX_SIZE * particle.get_scale()) // 2
            y0 = h - (center[1] - (BOX_SIZE * particle.get_scale()) // 2)
            x1 = center[0] + (BOX_SIZE * particle.get_scale()) // 2
            y1 = h - (center[1] + (BOX_SIZE * particle.get_scale()) // 2)
            draw_rectangle(x0, y0, x1, y1, img_arr, particle.color)
    return img_arr
