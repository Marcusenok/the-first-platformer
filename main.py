import pygame, sys

pygame.init()
screen = pygame.display.set_mode((700, 1000))

FPS = 50

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ['', '', '',
        '            Описание истории и маленькое описание управления']

    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (700, 1000))
    screen.blit(fon, (0, 0))
    a = pygame.font.Font(None, 30)
    text_coord = 50
    pygame.display.set_caption("Платформер")
    for line in intro_text:
        string_rendered = a.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return main()
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Платформер")
    bg = pygame.Surface((1200, 800))
    bg.fill(pygame.Color('black'))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            screen.blit(bg, (0, 0))
            pygame.display.update()


if __name__ == "__main__":
    start_screen()
