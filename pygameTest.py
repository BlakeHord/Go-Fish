import pygame
from math import pi

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 225)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example Code")

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

    pygame.draw.lines(screen, RED, False, [[10, 80], [10, 180], [50, 180], [50, 140], [40, 130], [10, 130], [40, 130], [50, 120], [50, 90], [40, 80], [10, 80], 5])
    pygame.draw.lines(screen, BLUE, False, [[60, 80], [60, 180], [100, 180], 5])
    pygame.draw.lines(screen, GREEN, False, [[110, 180], [110, 80], [150, 80], [150, 180], [150, 140], [110, 140], 5])
    #pygame.draw.lines(screen, RED, False, [[160, ]])

    pygame.display.flip()

pygame.quit()
