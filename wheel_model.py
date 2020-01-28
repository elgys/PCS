import pymunk
import human_model
from pymunk.vec2d import Vec2d
import numpy as np


WHEEL_RING_MASS = 22.0 # kg, total mass should be around 55 total
WHEEL_RADIUS = 105.0 # cm
WHEEL_WIDTH = 4.0 # cm
GRAVITY_CONSTANT = -982 # kg/s

RHONRAD_PIECE_AMOUNT = 100 # segments of the outer ring
PLANK_WIDTH = 9.0 # cm

# WHEEL_PLANK_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_PLANK_ANGLE = 12.37 * np.pi/180
WHEEL_PLANK_MASS = 7.0 # kg per plank
# WHEEL_SIDE+SPOKE_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_SIDE_SPOKE_ANGLE = 77.47 * np.pi/180
WHEEL_SIDE_SPOKE_MASS = 3.0 # kg per spoke
# WHEEL_UPPER_SPOKE_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_UPPER_SPOKE_ANGLE = 130.01 * np.pi/180
WHEEL_UPPER_SPOKE_MASS = 5.5 # kg per spoke
# WHEEL_TOP_SPOKE_ANGLE = degrees * pi/180 = rad, angle from straight down, each way
WHEEL_TOP_SPOKE_ANGLE = 180 * np.pi/180
WHEEL_TOP_SPOKE_MASS = 2.0 # kg sole top spoke

FLOOR_RADIUS = 0.4 # cm
# FLOOR_WIDTH in cm, max rotations allowed is 2 full rotations each way (wheel gym competition rules)
FLOOR_WIDTH = 2 * np.pi * WHEEL_RADIUS * 4.2

COULOMB_FRICTION_CONSTANT = 0.7 # The friction coefficient for PVC on wood

DT = 0.01 # seconds, time difference between simulation steps

#placement of the wheel in the space.
WHEEL_MIDDLE = Vec2d(700, WHEEL_RADIUS + FLOOR_RADIUS + WHEEL_WIDTH)


class Wheel_model:
    def __init__(self,time):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, GRAVITY_CONSTANT) # Generic gravity
        self.space.damping = 0.99 # Generic resistance
        self.entities = []
        self.entity_addresses = {}
        self.human_body = []
        self.max_run_time = time

        self.__setup_rhonrad()
        self.__setup_floor()
        self.space.add(self.entities)

        self.current_time = 0.0 # seconds
        self.max_angle = 0.0
        self.forces = [] # [[force vector, location vector, end_time]]
        self.angle_actions = [] # [[angle, f, *args]]
        self.run_simulation = True

    def __setup_floor(self):
        """ Setup the static floor beneath the wheel."""
        floor = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor.position = (0.0, 0.0)
        floor.start_position = Vec2d(floor.position)

        shape = pymunk.Segment(floor, (-FLOOR_WIDTH/2, 0),
                               (FLOOR_WIDTH/2, 0), FLOOR_RADIUS)
        shape.friction = COULOMB_FRICTION_CONSTANT

        self.entities += [floor, shape]
        self.entity_addresses['floor'] = floor

    def __setup_rhonrad(self):
        """ Setup the wheel with its ring, planks and spokes using the constants
            above as template."""
        moment = pymunk.moment_for_circle(
            WHEEL_RING_MASS, WHEEL_RADIUS - (2 * WHEEL_WIDTH), WHEEL_RADIUS)
        rhonrad = pymunk.Body(moment=moment)
        rhonrad.position = WHEEL_MIDDLE
        rhonrad.start_position = Vec2d(rhonrad.position)
        self.entities.append(rhonrad)
        self.entity_addresses['rhonrad'] = rhonrad

        self.__setup_rhonrad_ring(rhonrad)
        self.__setup_rhonrad_planks(rhonrad)
        self.__setup_rhonrad_spokes(rhonrad)
        self.rhonrad = rhonrad

    def __setup_rhonrad_ring(self, rhonrad):
        """ Setup the shape of the outer ring of the wheel."""
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

    def __setup_rhonrad_planks(self, rhonrad):
        """ Setup the shapes and the mass of the lower planks."""
        self.__setup_wheight_point_rhonrad(
            rhonrad, WHEEL_PLANK_MASS, WHEEL_PLANK_ANGLE, name='plank')

    def __setup_rhonrad_spokes(self, rhonrad):
        """ Setup the shapes and the mass of the spokes"""
        self.__setup_wheight_point_rhonrad(
            rhonrad, WHEEL_SIDE_SPOKE_MASS, WHEEL_SIDE_SPOKE_ANGLE, name='lower_spoke')
        self.__setup_wheight_point_rhonrad(
            rhonrad, WHEEL_UPPER_SPOKE_MASS, WHEEL_UPPER_SPOKE_ANGLE, name='upper_grip')
        self.__setup_wheight_point_rhonrad(
            rhonrad, WHEEL_TOP_SPOKE_MASS, WHEEL_TOP_SPOKE_ANGLE, amount=1, name='top_grip')

    def __setup_wheight_point_rhonrad(self, rhonrad, mass_per, angle, amount=2, name='', inner_offset=4):
        """ Setup (a) weighted point(s) on the wheel, with the given mass per
            point, at angle from the bottom.
            Inner offset can be used to offset the points to the inside to show
            the spokes and planks more easily in the visualization."""
        entities = []

        for i in range(amount):
            point_pos = Vec2d((WHEEL_RADIUS - inner_offset) * np.sin(angle * (-1) ** i),
                              (WHEEL_RADIUS - inner_offset) * -np.cos(angle * (-1) ** i))
            point = pymunk.Circle(rhonrad, abs(inner_offset), point_pos)
            point.mass = mass_per
            entities.append(point)

            if name:
                self.entity_addresses[name + '_' + str(2 - i)] = point

        self.entities += entities

    def set_human(self,human):
        """ Setup the gymnast in the wheel."""
        if self.human_body:
            self.space.remove(self.human_body)

        human.rightFootOnMiddel(self.entity_addresses["plank_1"].offset)

        places = human.test_bodypositions()
        human_body = []
        #shoulderline
        human_body.append(pymunk.Segment(self.rhonrad,places[1],places[4],1))
        #left arm
        human_body.append(pymunk.Segment(self.rhonrad,places[1],places[2],1))
        human_body.append(pymunk.Segment(self.rhonrad,places[2],places[3],1))
        #right arm
        human_body.append(pymunk.Segment(self.rhonrad,places[4],places[5],1))
        human_body.append(pymunk.Segment(self.rhonrad,places[5],places[6],1))
        #hips
        human_body.append(pymunk.Segment(self.rhonrad,places[1],places[7],1))
        human_body.append(pymunk.Segment(self.rhonrad,places[4],places[10],1))
        human_body.append(pymunk.Segment(self.rhonrad,places[7],places[10],1))
        #left leg
        human_body.append(pymunk.Segment(self.rhonrad,places[7],places[8],1))
        human_body.append(pymunk.Segment(self.rhonrad,places[8],places[9],1))
        #right leg
        human_body.append(pymunk.Segment(self.rhonrad,places[10],places[11],1))
        human_body.append(pymunk.Segment(self.rhonrad,places[11],places[12],1))

        self.set_human_center_of_mass(human.getcog(),mass = human.getweigth())
        self.human_body = human_body
        self.space.add(human_body)

    def set_human_center_of_mass(self, center_of_mass, mass=-1):
        """ Set the center of mass for the human in the wheel, changing the mass
            if the human somehow changes weight (or dissapears out of the
            wheel)."""
        if 'human' not in self.entity_addresses:
            human = pymunk.Circle(
                self.entity_addresses['rhonrad'], 1, center_of_mass)
            self.entity_addresses['human'] = human
            self.space.add(human)
        else:
            human = self.entity_addresses['human']
            human.unsafe_set_offset(center_of_mass)

        if mass != -1:
            human.mass = mass

    def get_named_location(self, name):
        """ Get the location of the entity relative to the middle of the wheel."""
        return self.entity_addresses[name].offset

    def get_max_angle(self):
        return self.max_angle

    def add_force_on_wheel(self, force_vector_direction, force_strength, location, time=-1):
        """ Adds a force to the wheel in the given direction with the given
            strength at the relative (to the wheel's center) location given."""
        force_vector_direction = np.array(
            force_vector_direction) / np.linalg.norm(force_vector_direction)
        force_vector = force_vector_direction * force_strength

        if time >= 0:
            end_time = self.current_time + time
        else:
            end_time = -1

        force = [force_vector, location, end_time]
        self.forces.append(force)

        return force

    def add_force_on_wheel_named(self, name, force_strength):
        """ Adds a force at the postion of a named entity."""
        location = self.entity_addresses[name].offset

        return self.add_force_on_wheel(location, force_strength, location)

    def remove_force_on_wheel(self, force):
        """ Remove the force added by add_force_on_wheel from the wheel.
            force argument is expected to be the force vector from the
            add_force_on_wheel function."""
        force_vector, location, end_time = force

        self.forces.remove(force)

    def remove_all_forces(self):
        """ Removes all forces currently working on the wheel."""
        self.forces = []

    def add_angle_action(self, angle, f, *args):
        """ Add a angle action to the model which triggers function f with
            arguments *args when the wheel has turned angle radians."""
        self.angle_actions.append([angle, f, *args])

    def run_failure(self):
        """ Helper function to indicate that the simulation was a failure, and
            to stop the simulation."""
        self.success = False
        self.run_simulation = False

    def run_success(self):
        """ Helper function to indicate that the simulation was a success, and
            to stop the simulation."""
        self.success = True
        self.run_simulation = False

    def __apply_angle_actions(self, ordered=True):
        """ Apply function f with arguments args when the wheel has turned angle
            radians."""
        to_remove = []

        if ordered:
            for angle_action in self.angle_actions:
                angle, f, *args = angle_action

                if abs(self.entity_addresses['rhonrad'].angle) > angle:
                    f(*args)
                    to_remove.append(angle_action)
                else:
                    break
        else:
            for angle_action in self.angle_actions:
                angle, f, *args = angle_action

                if abs(self.entity_addresses['rhonrad'].angle) > angle:
                    f(*args)
                    to_remove.append(angle_action)

        for angle_action in to_remove:
            self.angle_actions.remove(angle_action)

    def __apply_forces(self):
        """ Apply all forces currently acting on the wheel."""
        to_remove = []

        for [force_vector, location, end_time] in self.forces:
                self.entity_addresses['rhonrad'].apply_force_at_local_point(
                force_vector, location)
                if end_time != -1 and end_time >= self.current_time:
                    to_remove = [force_vector, location, end_time]

        for force in to_remove:
            self.remove_force_on_wheel(force)


    def step(self):
        """ Take a step in the simulation; also apply all angle actions
            (actions which occur after a specified angle) and apply all forces
            currently working on the wheel which are not gravity or friction."""
        self.__apply_angle_actions()
        self.__apply_forces()
        self.space.step(DT)
        self.current_time += DT

        if self.max_angle < abs(self.entity_addresses['rhonrad'].angle):
            self.max_angle = abs(self.entity_addresses['rhonrad'].angle)

        if self.current_time > self.max_run_time:
            self.run_failure()

        return self.run_simulation
