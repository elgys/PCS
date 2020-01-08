import pymunk
from pymunk.vec2d import Vec2d

WHEEL_MASS = 30.0  # 55 total
WHEEL_RADIUS = 105.0
DT = 0.05


class Model:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -98.200)  # Generic gravity
        self.space.damping = 0.99      # Generic resistance
        self.setup_floor()
        self.setup_rhonrad()

    def setup_floor(self):
        floor = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor.position = (0.0, 0.0)
        floor.start_position = Vec2d(floor.position)

        shape = pymunk.Segment(floor, (-600, 0), (600, 0), 5)

        self.space.add(floor, shape)

    def setup_rhonrad(self):
        moment = pymunk.moment_for_circle(
            WHEEL_MASS, WHEEL_RADIUS*0.97, WHEEL_RADIUS)
        rhonrad = pymunk.Body(WHEEL_MASS, moment)
        rhonrad.position = (0.0, WHEEL_RADIUS + 6)
        rhonrad.start_position = Vec2d(rhonrad.position)

        shape = pymunk.Circle(rhonrad, WHEEL_RADIUS)
        self.space.add(rhonrad, shape)

    def step(self):
        self.space.step(DT)
