import pymunk
from pymunk.vec2d import Vec2d
import numpy as np


WHEEL_RING_MASS = 22.0  # kg, total mass should be ~55 total
WHEEL_RADIUS = 105.0  # cm
WHEEL_WIDTH = 4.0  # cm
GRAVITY_CONSTANT = -98.2/10  # kg/s

RHONRAD_PIECE_AMOUNT = 50  # segments of the outer ring
PLANK_WIDTH = 9.0  # cm

# WHEEL_PLANK_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_PLANK_ANGLE = 12.37 * np.pi/180
WHEEL_PLANK_MASS = 7.0  # kg per plank
# WHEEL_SIDE+SPOKE_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_SIDE_SPOKE_ANGLE = 77.47 * np.pi/180
WHEEL_SIDE_SPOKE_MASS = 3.0  # kg per spoke
# WHEEL_UPPER_SPOKE_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_UPPER_SPOKE_ANGLE = 130.01 * np.pi/180
WHEEL_UPPER_SPOKE_MASS = 5.5  # kg per spoke
# WHEEL_TOP_SPOKE_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_TOP_SPOKE_ANGLE = 180 * np.pi/180
WHEEL_TOP_SPOKE_MASS = 2.0  # kg sole top spoke

FLOOR_RADIUS = 0.4  # cm, not that interesting
# FLOOR_WIDTH in cm, max rotations allowed is 2 full rotations each way (rhonrad rules)
FLOOR_WIDTH = 2 * np.pi * WHEEL_RADIUS * 4.2

COULOMB_FRICTION_CONSTANT = 1  # The friction coefficient for PVC on wood

DT = 0.01  # seconds, time difference between frames

WHEEL_MIDDLE = Vec2d(300, WHEEL_RADIUS + FLOOR_RADIUS + WHEEL_WIDTH)


class Model:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, GRAVITY_CONSTANT)  # Generic gravity
        self.space.damping = 0.99          # Generic resistance
        self.entities = []
        self.entity_names = {}
        self._setup_rhonrad()
        self._setup_floor()
        self.space.add(self.entities)
        print(self.entity_names['rhonrad'].mass,
              self.entity_names['rhonrad'].moment)

    def _setup_floor(self):
        floor = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor.position = (0.0, 0.0)
        floor.start_position = Vec2d(floor.position)

        shape = pymunk.Segment(floor, (-FLOOR_WIDTH/2, 0),
                               (FLOOR_WIDTH/2, 0), FLOOR_RADIUS)
        shape.friction = COULOMB_FRICTION_CONSTANT

        self.entities += [floor, shape]
        self.entity_names['floor'] = floor

    def _setup_rhonrad(self):
        """Setup the rhonrad with its ring, planks and spokes made in a way
        the constants above the file as template. To see how the rhonrad looks
        like in the engine, run 'screen_test.py'."""
        moment = pymunk.moment_for_circle(
            WHEEL_RING_MASS, WHEEL_RADIUS - (2 * WHEEL_WIDTH), WHEEL_RADIUS)
        rhonrad = pymunk.Body(moment=moment)
        rhonrad.position = WHEEL_MIDDLE
        rhonrad.start_position = Vec2d(rhonrad.position)
        self.entities.append(rhonrad)
        self.entity_names['rhonrad'] = rhonrad

        self._setup_rhonrad_ring(rhonrad)
        self._setup_rhonrad_planks(rhonrad)
        self._setup_rhonrad_spokes(rhonrad)

    def _setup_rhonrad_ring(self, rhonrad):
        """Setup the shape of the outer ring of the rhonrad."""
        ring = []
        a = WHEEL_RADIUS
        angle = np.exp(2j * np.pi / RHONRAD_PIECE_AMOUNT)
        for i in range(RHONRAD_PIECE_AMOUNT - 1):
            b = angle * a
            ring.append(pymunk.Segment(
                rhonrad, (np.real(a), np.imag(a)), (np.real(b), np.imag(b)), WHEEL_WIDTH))
            a = b
        ring.append(pymunk.Segment(
            rhonrad, (np.real(a), np.imag(a)), Vec2d(WHEEL_RADIUS, 0.0), WHEEL_WIDTH))

        piece_mass = WHEEL_RING_MASS / RHONRAD_PIECE_AMOUNT
        for segment in ring:
            segment.friction = COULOMB_FRICTION_CONSTANT
            segment.mass = piece_mass

        self.entities += ring

    def _setup_rhonrad_planks(self, rhonrad):
        """Setup theshapes (and most importantly the mass) of the lower planks
        of the rhonrad"""
        self._setup_wheight_point_rhonrad(
            rhonrad, WHEEL_PLANK_MASS, WHEEL_PLANK_ANGLE, name='plank')

    def _setup_rhonrad_spokes(self, rhonrad):
        """Setup the shapes (and most importantly the mass) of the spokes"""
        self._setup_wheight_point_rhonrad(
            rhonrad, WHEEL_SIDE_SPOKE_MASS, WHEEL_SIDE_SPOKE_ANGLE, name='lower_spoke')
        self._setup_wheight_point_rhonrad(
            rhonrad, WHEEL_UPPER_SPOKE_MASS, WHEEL_UPPER_SPOKE_ANGLE, name='upper_grip')
        self._setup_wheight_point_rhonrad(
            rhonrad, WHEEL_TOP_SPOKE_MASS, WHEEL_TOP_SPOKE_ANGLE, amount=1, name='top_grip')

    def _setup_wheight_point_rhonrad(self, rhonrad, mass_per, angle, amount=2, name=''):
        """Setup (a) weighted point(s) on the rhonrad, with the given mass_per point,
        at angle from the bottom."""
        entities = []
        for i in range(amount):
            point_pos = Vec2d((WHEEL_RADIUS - 4) * np.sin(angle * (-1) ** i),
                              (WHEEL_RADIUS - 4) * -np.cos(angle * (-1) ** i))
            point = pymunk.Circle(rhonrad, 4, point_pos)
            point.mass = mass_per
            entities.append(point)
            if name:
                self.entity_names[name + '_' + str(i)] = point

        self.entities += entities

    def step(self):
        """Take a step in the simulation"""
        self.space.step(DT)
