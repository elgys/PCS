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
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    def __init__(self,sim):
        # Space
        self._space = sim.w_model.space
        # self._space.gravity = (0.0, -900.0)

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
        self._space.debug_draw(self._draw_options)

        # Execution control and time until the next ball spawns
        self._running = True

    def run(self):
        """
        The main loop of the game.
        :return: None
        """
        # Main loop

        while self._running:
            # Progress time forward

            for x in range(self._physics_steps_per_frame):
                # self._space.step(self._dt)
                self._m.step()

            self._process_events()
            # self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(1)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))


    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)