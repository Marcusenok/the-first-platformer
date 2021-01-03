import pygame

pygame.init()
screen = pygame.display.set_mode((700, 1000))


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

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return main()
        pygame.display.flip()


MOVE_SPEED = 15
JUMP_POWER = 20
GRAVITY = 1.6


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((30, 50))
        self.image.fill(pygame.Color('red'))
        self.rect = pygame.Rect(x, y, 30, 50)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?

    def update(self, left, right, up, platforms):
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
        self.collide(self.xvel, 0, platforms)
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(pygame.Color(0, 255, 255))
        self.rect = pygame.Rect(x, y, 30, 30)


class Camera(object):
    def __init__(self, camera_func):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, 50000, 50000)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = l, t = -l + 700 / 2, -t + 900 / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width), l)  # Не движемся дальше правой границы
    t = max(-(camera.height), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    bg = pygame.Surface((1200, 800))
    bg.fill(pygame.Color('black'))
    timer = pygame.time.Clock()
    player = Player(50, 1500)
    left = right = False
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(player)
    level = open('level.txt', 'r')
    x = y = 0
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "p":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += 30  # блоки платформы ставятся на ширине блоков
        y += 30  # то же самое и с высотой
        x = 0

    camera = Camera(camera_configure)

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
        player.update(left, right, up, platforms)
        camera.update(player)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()


if __name__ == "__main__":
    start_screen()