import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # no window border
pygame.display.set_caption("Snack Attack")
pygame.mouse.set_visible(False)

# Colors
SOFT_BLACK = (20, 20, 20)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BRICK = (178, 34, 34)
MUSHROOM_RED = (255, 80, 80)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)

# Game settings
block_size = 20
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

def draw_snake(snake_list, boost_active):
    color = YELLOW if boost_active else GREEN
    for segment in snake_list:
        pygame.draw.rect(screen, color, [segment[0], segment[1], block_size, block_size])

def draw_score(score, level):
    text = font.render(f"Score: {score} | Level: {level}", True, WHITE)
    screen.blit(text, [10, 10])

def draw_pause_message():
    text = font.render("PAUSED - Press Space to Resume", True, GRAY)
    screen.blit(text, [WIDTH // 2 - 200, HEIGHT // 2])

def draw_barriers(barriers):
    for b in barriers:
        pygame.draw.rect(screen, BRICK, [b[0], b[1], block_size, block_size])

def draw_mushroom(x, y):
    center = (x + block_size // 2, y + block_size // 2)
    pygame.draw.circle(screen, MUSHROOM_RED, center, block_size // 2)

def generate_barriers(level):
    barriers = []
    margin = block_size * 3
    if level < 2:
        return barriers
    if level == 2:
        for y in range(margin, HEIGHT - margin, block_size):
            barriers.append([WIDTH // 2, y])
    elif level == 3:
        for x in range(margin, WIDTH - margin, block_size):
            barriers.append([x, HEIGHT // 3])
            barriers.append([x, 2 * HEIGHT // 3])
    elif level == 4:
        for y in range(margin, HEIGHT // 2, block_size):
            barriers.append([WIDTH // 4, y])
        for x in range(WIDTH // 4, WIDTH // 2, block_size):
            barriers.append([x, HEIGHT // 2])
    elif level >= 5:
        for x in range(margin, WIDTH - margin, block_size):
            barriers.append([x, margin])
            barriers.append([x, HEIGHT - margin])
        for y in range(margin, HEIGHT - margin, block_size):
            barriers.append([margin, y])
            barriers.append([WIDTH - margin, y])
    return barriers

def generate_safe_food(snake, barriers):
    while True:
        x = round(random.randrange(0, WIDTH - block_size) / block_size) * block_size
        y = round(random.randrange(0, HEIGHT - block_size) / block_size) * block_size
        too_close_to_score = x < 160 and y < 60  # avoid score area
        if [x, y] not in snake and [x, y] not in barriers and not too_close_to_score:
            return x, y

def game_loop():
    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = block_size, 0

    snake = []
    snake_length = 1
    score = 0
    level = 1

    speed = 10
    boost_active = False
    boost_counter = 0

    barriers = generate_barriers(level)
    food_x, food_y = generate_safe_food(snake, barriers)

    paused = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif not paused:
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -block_size
                        y_change = 0
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = block_size
                        y_change = 0
                    elif event.key == pygame.K_UP and y_change == 0:
                        x_change = 0
                        y_change = -block_size
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        x_change = 0
                        y_change = block_size

        if not paused:
            x += x_change
            y += y_change

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                running = False

            if x == food_x and y == food_y:
                snake_length += 1
                score += 1

                if score % 10 == 0:
                    level += 1
                    barriers = generate_barriers(level)

                if score % 15 == 0:
                    boost_active = True
                    boost_counter = 50

                food_x, food_y = generate_safe_food(snake, barriers)

            if boost_active:
                boost_counter -= 1
                if boost_counter <= 0:
                    boost_active = False

            snake.append([x, y])
            if len(snake) > snake_length:
                del snake[0]

            for segment in snake[:-1]:
                if segment == [x, y]:
                    running = False

            for b in barriers:
                if [x, y] == b:
                    running = False

        screen.fill(SOFT_BLACK)
        draw_barriers(barriers)
        draw_mushroom(food_x, food_y)
        draw_snake(snake, boost_active)
        draw_score(score, level)
        if paused:
            draw_pause_message()

        pygame.display.update()
        clock.tick(20 if boost_active else speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()

