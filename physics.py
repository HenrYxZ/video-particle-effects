class Transform:
    def __init__(self, position, scale=1):
        """
        Attributes:
            position(ndarray): 2D position
            scale(ndarray): 2D scale of the particle
        """
        self.position = position
        self.scale = scale


class State:
    def __init__(self, transform, v, m=1):
        """
        Attributes:
            transform(Transform): Transform of the object (position, scale,
                rotation, etc.)
            v(ndarray): Velocity of the object
            m(float): Mass of the object
        """
        self.transform = transform
        self.v = v
        self.m = m

    def __str__(self):
        return f'transform= {self.transform}, v= {self.v}, m= {self.m}'

    def __repr__(self):
        return f'transform= {self.transform}, v= {self.v}, m= {self.m}'


class RigidBody:
    def __init__(self, state):
        """
        Args:
            state(State): Current state of the body
        """
        self.state = state

    def get_position(self):
        return self.state.transform.position

    def next_state(self, delta_time, force):
        """
        Args:
            delta_time(float): Amount of time elapsed from previous state
            force(ndarray): Vector of force applied to the body

        Returns:
             State: the next state of the body
        """
        distance = self.state.v * delta_time
        position = self.get_position() + distance
        a = force / self.state.m
        v = self.state.v + a * delta_time
        transform = Transform(position)
        next_state = State(transform, v)
        return next_state


class Simulation:
    def __init__(self, rigid_bodies, duration, time_step):
        """
        A physical simulation of rigid bodies through certain time

        Attributes:
            rigid_bodies(list): The bodies that are part of the system
            duration(float): How much time in seconds the simulation last
            time_step(float): Seconds that pass between each simulation step
        """
        self.rigid_bodies = rigid_bodies
        self.duration = duration
        self.time_step = time_step

    def run(self, force):
        pass
