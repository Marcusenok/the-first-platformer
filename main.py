import pygame, sys

pygame.init()
screen = pygame.display.set_mode((700, 1000))

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['', '', '', '            Описание истории и маленькое описание управления',
                  '                         Нажмите любую кнопку чтобы начать']

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


MOVE_SPEED = 20
WIDTH = 60
HEIGHT = 71
JUMP_POWER = 10
GRAVITY = 0.35


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = pygame.image.load('gg.png')
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?

    def update(self, left, right, up):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
        self.rect.x += self.xvel  # переносим свои положение на xvel
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    bg = pygame.Surface((1200, 800))
    bg.fill(pygame.Color('black'))
    timer = pygame.time.Clock()
    player = Player(30, 500)
    left = right = False
    up = False

    run = True
    while run:
        timer.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False

        screen.blit(bg, (0, 0))
        player.update(left, right, up)
        player.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    start_screen()