import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы игры
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 2, 2

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")

# Часы для контроля FPS
clock = pygame.time.Clock()


# Классы для ракетки и мяча
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0

    def move(self, up=True):
        if up:
            self.rect.y = max(self.rect.y - PADDLE_SPEED, 0)
        else:
            self.rect.y = min(self.rect.y + PADDLE_SPEED, HEIGHT - PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-1, 1]) * BALL_SPEED_X
        self.dy = random.choice([-1, 1]) * BALL_SPEED_Y

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
            if self.rect.left <= 0:
                right_paddle.score += 1
            else:
                left_paddle.score += 1

            self.reset()

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = random.choice([-1, 1]) * BALL_SPEED_X
        self.dy = random.choice([-1, 1]) * BALL_SPEED_Y


# Создание объектов игры
left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
right_paddle = Paddle(WIDTH - 25, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Управление ракетками
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)

    # Движение мяча и проверка столкновений
    ball.move()
    if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
        ball.dx *= -1

    # Отрисовка
    screen.fill(BLACK)
    left_paddle.draw()
    right_paddle.draw()
    ball.draw()

    # Отрисовка счета
    font = pygame.font.Font(None, 36)
    left_score_text = font.render(str(left_paddle.score), True, WHITE)
    right_score_text = font.render(str(right_paddle.score), True, WHITE)
    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()