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


class BouncyBalls(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Balls appear occasionally and drop onto the platform. They bounce around.
    """

    def __init__(self):
        # Space
        self._m = wheel_model.Wheel_model()
        human = human_model.human(160,55,list([0,0]),40)
        right_foot_location = self._m.get_named_location("plank_1")
        human.setturned(True)
        human.positionchange(0,343, 30,30,210,210,15,15,347,347)
        print(human.test_bodypositions())
        human.rightFootOnMiddel(right_foot_location)
        print(human.getcog())
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
        self._screen = pygame.display.set_mode((1200, 400))
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        self._draw_options.DRAW_SHAPE= True
        self._space.debug_draw(self._draw_options)
        # Static barrier walls (lines) that the balls bounce off of
        # self._add_static_scenery()

        # Balls that exist in the world
        # self._balls = []

        # Execution control and time until the next ball spawns
        self._running = True
        # self._ticks_to_next_ball = 10

    def run(self):
        """
        The main loop of the game.
        :return: None
        """
        # Main loop

        pushed = 0
        # print(self._m.add_force_on_wheel((1, 0), 5800, (0, -30)))
        # print(self._m.forces[0])

        while self._running:
            # Progress time forward
            if pushed >= 0:
                pushed += 1
            if pushed >= 20:
                # print(self._m.entity_addresses['rhonrad'].center_of_gravity)
                # print(self._m.entity_addresses['rhonrad'].angle % 6.282)
                # self._m.entity_addresses['rhonrad'].apply_force_at_local_point(
                #     (0, -5400), (105, 0))
                pass
            if pushed >= 200:
                # self._m.entity_addresses['rhonrad'].angle = 3.14159
                # self._m.set_human_center_of_mass((40, -80), 55)
                pushed = -1

            for x in range(self._physics_steps_per_frame):
                # self._space.step(self._dt)
                self._m.step()

            self._process_events()
            # self._update_balls()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()
            # Delay fixed time between frames
            self._clock.tick(50)
            pygame.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _add_static_scenery(self):
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [pymunk.Segment(static_body, (111.0, 280.0), (407.0, 246.0), 0.0),
                        pymunk.Segment(static_body, (407.0, 246.0), (407.0, 343.0), 0.0)]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self._space.add(static_lines)

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

    def _update_balls(self):
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0:
            self._create_ball()
            self._ticks_to_next_ball = 100
        # Remove balls that fall below 100 vertically
        balls_to_remove = [
            ball for ball in self._balls if ball.body.position.y < 100]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def _create_ball(self):
        """
        Create a ball.
        :return:
        """
        mass = 10
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(115, 350)
        body.position = x, 400
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 0.9
        self._space.add(body, shape)
        self._balls.append(shape)

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


if __name__ == '__main__':
    game = BouncyBalls()
    game.run()
