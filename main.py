import pygame
from pygame import *

WIN_WIDTH = 1200
WIN_HEIGHT = 800
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Платформер")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color('red'))

    run = True
    while run:
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
        screen.blit(bg, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
