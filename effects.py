import numpy as np
import time

# Local Modules
from constants import MAX_VALUE
from particle import Particle, Shape
from physics import create_body_at


PARTICLES_LIFE_SPAN = 2
DEFAULT_PARTICLE_COLOR = np.array([MAX_VALUE, 0, 0], dtype=int)


def particle_effects(keypoints, particles, delta_time, w, h):
    """
    Handle particle effects for a frame
    Args:
        keypoints(List[ndarray]): List of 2D points
    Returns:
        List[Particle]: the new particles
    """
    current_time = time.time()
    # Only use the particles that are alive
    particles = list(
        filter(lambda elem: elem.is_alive(current_time), particles)
    )
    for particle in particles:
        percent = (current_time - particle.creation_time) / particle.life_span
        # Fade out in time
        particle.color = particle.color * (1 - percent)
        # Decrease size in time
        particle.rigid_body.state.transform.scale = 1 - percent
        # move by force
        f = np.array([350, -120])
        particle.rigid_body.state = particle.rigid_body.next_state(
            delta_time, f
        )
    particles = list(
        filter(lambda elem: elem.is_on_screen(w, h), particles)
    )
    for point in keypoints:
        rigid_body = create_body_at(point)
        color = DEFAULT_PARTICLE_COLOR
        particle = Particle(
            rigid_body, color, Shape.CIRCLE, PARTICLES_LIFE_SPAN, current_time
        )
        particles.append(particle)
    return particles
