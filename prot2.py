import pygame

pygame.init()
screen = pygame.display.set_mode((775, 400))
pygame.mixer.music.load("music.mp3")


def start_screen():
    intro_text = ['                                          Здаров захожий!',
                  '    Я сделал для тебя игру и играть в благородство играть не собираюсь',
                  'Чтобы выжить в этом опасном мире тебе придётся научится полагаться',
                  'только на себя. Запомни что двигаешься ты только на стрелочки и никаких',
                  'тебе WASD усёк! Дальше, твоя задача пройти три испытания и добраться',
                  'до конца живым и невредимым. Будь осторожен на уровнях есть',
                  'смертельные ловушки на которые не желательно напарываться.',
                  'Давай быстренько метнулся кабанчиком туда обратно в темпе, в темпе!!!']
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (800, 1000))
    screen.blit(fon, (0, 0))
    a = pygame.font.Font(None, 30)
    text_coord = 50
    pygame.display.set_caption("Платформер")
    bt = Button()
    bt.create_button(screen, (255, 0, 225), 30, 330, 100, 40, 100, '1 lvl', (0, 255, 0))
    bt1 = Button()
    bt1.create_button(screen, (255, 0, 225), 330, 330, 100, 40, 100, '2 lvl', (0, 255, 0))
    bt2 = Button()
    bt2.create_button(screen, (255, 0, 225), 630, 330, 100, 40, 100, '3 lvl', (0, 255, 0))
    for line in intro_text:
        string_rendered = a.render(line, 1, pygame.Color(200, 200, 255))
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                print(mouse_pos)
                bt.pressed(mouse_pos)
                bt1.pressed(mouse_pos)
                bt2.pressed(mouse_pos)
        pygame.display.flip()


MOVE_SPEED = 19
JUMP_POWER = 14
GRAVITY = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((22, 22))
        self.image.fill(pygame.Color('red'))
        self.rect = pygame.Rect(x, y, 22, 22)  # прямоугольный объект
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
                if isinstance(p, BlockDie):  # если пересакаемый блок - blocks.BlockDie или Monster
                    self.die()  # умираем

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

    def die(self):
        pygame.time.wait(500)
        self.teleporting(50, 1000)  # перемещаемся в начальные координаты

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(pygame.Color(0, 255, 255))
        self.rect = pygame.Rect(x, y, 22, 22)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.Surface((10, 10))
        self.image = pygame.image.load('chip_.png')
        self.rect = pygame.Rect(x, y, 10, 10)


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
    screen = pygame.display.set_mode((900, 660))
    bg = pygame.Surface((1000, 2000))
    bg.fill(pygame.Color('black'))
    pygame.mixer.music.play(-1)
    flPause = False
    timer = pygame.time.Clock()
    player = Player(50, 1600)
    left = right = False
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(player)
    level = open('level_1.txt', 'r')
    x = y = 0
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "p":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            x += 22  # блоки платформы ставятся на ширине блоков
        y += 22  # то же самое и с высотой
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        screen.blit(bg, (0, 0))
        player.update(left, right, up, platforms)
        camera.update(player)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print('Some button was pressed!')
                        return main()
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


if __name__ == "__main__":
    start_screen()
