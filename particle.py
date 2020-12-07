from enum import Enum
import time

# Local Modules
from constants import BOX_SIZE, CIRCLE_RADIUS
from physics import RigidBody


class Shape(Enum):
    BOX = 1
    CIRCLE = 2


class Particle:
    def __init__(self, rigid_body, color, shape, life_span, creation_time=None):
        """
        Attributes:
            rigid_body(RigidBody): The physical transform and state of the
                particle
            color(ndarray): Color for the particle (may include alpha)
            shape(Shape): The shape that this particle should have
            life_span(float): The amount of seconds this particle should live
            creation_time(float): Time on which the particle was created
        """
        self.rigid_body = rigid_body
        self.color = color
        self.shape = shape
        self.life_span = life_span
        if creation_time:
            self.creation_time = creation_time
        else:
            time.time()

    def get_position(self):
        return self.rigid_body.state.transform.position

    def get_scale(self):
        return self.rigid_body.state.transform.scale

    def is_alive(self, current_time):
        is_alive = current_time - self.creation_time < self.life_span
        return is_alive

    def is_on_screen(self, w, h):
        pos = self.get_position()
        side = max(BOX_SIZE / 2, CIRCLE_RADIUS)
        is_on_screen = side <= pos[0] < w - side and side <= pos[1] < h - side
        return is_on_screen
