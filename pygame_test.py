# https://gamedev.stackexchange.com/questions/126353/how-to-rotate-an-image-in-pygame-without-losing-quality-or-increasing-size-or-mo
import pygame

class Wheel(pygame.sprite.Sprite):

    def __init__(self, pos=(0,0), size=(250,250)):
        super(Wheel, self).__init__()
        self.o_image = pygame.image.load("./../Parallelstand.png").convert()
        self.image = self.o_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = 0

    def update(self, angle):
        self.image = pygame.transform.rotate(self.o_image, self.angle)
        self.angle = angle
        x,y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

def main():
    a = 0
    wheel = Wheel(pos=(125,125))

    while a < 360:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        wheel.update(a)
        screen.fill((0,0,0))
        screen.blit(wheel.image, wheel.rect)
        pygame.display.update()

        a += 0.1

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((250,250))
    main()
