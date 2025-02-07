import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Размеры объектов
WOLF_WIDTH = 80
WOLF_HEIGHT = 60
EGG_RADIUS = 10

# Скорость
WOLF_SPEED = 7
EGG_SPEED = 5

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лови яйца с волком")

# Часы для контроля FPS
clock = pygame.time.Clock()

# Шрифт для отображения счета
font = pygame.font.SysFont(None, 36)

# Загрузка изображений
try:
    wolf_image = pygame.image.load('wolf.png').convert_alpha()
    wolf_image = pygame.transform.scale(wolf_image, (WOLF_WIDTH, WOLF_HEIGHT))
except:
    # Если изображение не загружено, используем прямоугольник
    wolf_image = None

# Звуковые эффекты
try:
    catch_sound = pygame.mixer.Sound('catch.wav')
    egg_spawn_sound = pygame.mixer.Sound('egg_spawn.wav')
except:
    catch_sound = None
    egg_spawn_sound = None

# Класс для волка
class Wolf:
    def __init__(self):
        self.width = WOLF_WIDTH
        self.height = WOLF_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = WOLF_SPEED

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

    def draw(self, surface):
        if wolf_image:
            surface.blit(wolf_image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, BROWN, (self.x, self.y, self.width, self.height))

# Класс для яйца
class Egg:
    def __init__(self, type='normal'):
        self.radius = EGG_RADIUS
        self.x = random.randint(0, SCREEN_WIDTH - 2 * self.radius)
        self.y = -self.radius
        self.speed = EGG_SPEED
        self.type = type
        if self.type == 'bonus':
            self.color = GREEN
        elif self.type == 'penalty':
            self.color = RED
        else:
            self.color = YELLOW

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.radius

    def is_caught(self, wolf):
        return (self.x > wolf.x and self.x < wolf.x + wolf.width) and (self.y + self.radius > wolf.y)

# Функция для создания нового яйца
def create_egg(score):
    egg_type = random.choices(['normal', 'bonus', 'penalty'], weights=[80, 10, 10], k=1)[0]
    return Egg(type=egg_type)

# Инициализация объектов
wolf = Wolf()
eggs = []
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 1000)  # Каждую секунду появляется новое яйцо
score = 0
level = 1
egg_speed_increase = 0

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == spawn_event:
            egg = create_egg(score)
            eggs.append(egg)
            if egg_spawn_sound:
                egg_spawn_sound.play()

    # Обработка нажатий клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        wolf.move_left()
    if keys[pygame.K_RIGHT]:
        wolf.move_right()

    # Обновление яиц
    for egg in eggs[:]:
        egg.update()
        if egg.is_caught(wolf):
            if egg.type == 'bonus':
                score += 2
            elif egg.type == 'penalty':
                score -= 1
            else:
                score += 1
            if catch_sound:
                catch_sound.play()
            eggs.remove(egg)
        elif egg.is_off_screen():
            eggs.remove(egg)

    # Увеличение уровня сложности
    if score // 10 + 1 > level:
        level += 1
        EGG_SPEED += 1
        egg_speed_increase += 1

    # Отрисовка
    screen.fill(WHITE)
    wolf.draw(screen)
    for egg in eggs:
        egg.draw(screen)

    # Отображение счета и уровня
    score_text = font.render(f"Счет: {score}", True, BLACK)
    level_text = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)