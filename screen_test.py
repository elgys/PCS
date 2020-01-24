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
    """ This class is a debug class for the simulation.
        All code for visualization was taken from
        https://github.com/viblo/pymunk/blob/master/examples/bouncing_balls.py."""

    def __init__(self):
        # Space
        self._m = wheel_model.Wheel_model()
        human = human_model.human(160,55,list([0,0]),40)
        human.setturned(True)
        human.positionchange(0,343, 30,30,210,210,15,15,347,347)
        self._m.set_human(human)
        self._space = self._m.space
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

        # Execution control
        self._running = True

    def run(self):
        """ The main loop of the simulation."""
        # Main loop
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._m.step()

            self._process_events()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()

            # Delay fixed time between frames
            self._clock.tick(50)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self):
        """ Create the static bodies."""
        static_body = self._space.static_body
        static_lines = [pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0),
                        pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)]

        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(static_lines)

    def _process_events(self):
        """ Handle game and events like keyboard input. Call once per frame
            only."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")
    
    def _clear_screen(self):
        """ Clears the screen."""
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        """ Draw the objects."""
        self._space.debug_draw(self._draw_options)


if __name__ == '__main__':
    game = Debug()
    game.run()
