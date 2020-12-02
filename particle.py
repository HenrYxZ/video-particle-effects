from enum import Enum
import time

# Local Modules
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
