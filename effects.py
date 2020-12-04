import numpy as np
import time

# Local Modules
from constants import MAX_VALUE
from particle import Particle, Shape
from physics import create_body_at


PARTICLES_LIFE_SPAN = 1.5


def particle_effects(keypoints):
    """
    Handle particle effects for a frame
    Args:
        keypoints(List[ndarray]): List of 2D points
    Returns:
        List[Particle]: the new particles
    """
    current_time = time.time()
    # Only use the particles that are alive
    # particles = filter(lambda elem: elem.is_alive(), particles)
    particles = []
    for point in keypoints:
        rigid_body = create_body_at(point)
        color = np.array([MAX_VALUE, 0, 0])
        particle = Particle(
            rigid_body, color, Shape.BOX, PARTICLES_LIFE_SPAN
        )
        particles.append(particle)
    return particles
