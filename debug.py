import random
import human_model

# Library imports
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

# pymunk imports
import pymunk
import pymunk.pygame_util
import wheel_model


class Debug(object):
    """ This class is a debug class for the simulation."""

    def __init__(self, sim):
        # Space
        self.sim = sim

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((1000, 400))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._draw_options.DRAW_SHAPE= True
        self.sim.w_model.space.debug_draw(self._draw_options)


    def step_draw(self):
        """ Draws the current step in the simulation.
            It gets a simulation from init."""
        self._process_events()
        self._clear_screen()
        self._draw_objects()
        pygame.display.flip()
        pygame.display.set_caption("wheel simulation")

    def _process_events(self):
        """ Handle game and events like keyboard input. Call once per frame
            only."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self._screen, "wheel_capture.png")

    def _clear_screen(self):
        """ Clears the screen."""
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        """ Draw the objects."""
        self.sim.w_model.space.debug_draw(self._draw_options)
