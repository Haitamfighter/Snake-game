# Snake game version pygame
from snake import Snake
from fruit import Fruit
import random
import pygame
pygame.init()


# Screen settings
WIDTH, HEIGHT = 512, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
PSEUDO_WHITE = [random.randint(200, 255) for _ in range(3)]
PSEUDO_BLACK = [random.randint(0, 55) for _ in range(3)]
RAND_COLOR = [random.randint(0, 255) for _ in range(3)]
RED = (255, 0, 0)

# Choice images
choice_w = choice_h = WIDTH/5
limited_mode_img = pygame.transform.scale(pygame.image.load("assets/choice_imgs/limited_mode.jpg"), (choice_w, choice_h))
unlimited_mode_img = pygame.transform.scale(pygame.image.load("assets/choice_imgs/infinity_mode.png"), (choice_w, choice_h))

# Choice rects
limited_mode_rect = limited_mode_img.get_rect()
unlimited_mode_rect = unlimited_mode_img.get_rect()

# Functions
time = seconds = minutes = 0
def draw_screen():
    global time, seconds, minutes
    screen.fill(BLACK)

    font = pygame.font.SysFont("comicsans", 20)
    # Cuz 60 frames per second Smart hh
    time += 1
    if time == 60:
        seconds += 1
        time = 0
    if seconds == 60:
        minutes += 1
        seconds = 0
    txt_font = font.render(f"{minutes}:{seconds}", True, PSEUDO_WHITE)
    screen.blit(txt_font, ((WIDTH-txt_font.get_width())/2, 0))

    snake.draw(screen, PSEUDO_WHITE)
    for fruit in fruits:
        fruit.draw(screen)

    # Flip
    pygame.display.flip()


def draw_choice():
    screen.fill(WHITE)

    # Write
    font = pygame.font.SysFont("comicsans", 80)
    wlcmto_txt = font.render("Welcome To", True, BLACK)
    snakegame_txt = font.render("Snake Game", True, RAND_COLOR)
    screen.blit(wlcmto_txt, ((WIDTH-wlcmto_txt.get_width())/2, 0))
    screen.blit(snakegame_txt, ((WIDTH-snakegame_txt.get_width())/2, wlcmto_txt.get_height()))

    # Choice rects and images x & y
    fifth = WIDTH/5
    limited_mode_rect.x, limited_mode_rect.y = fifth, HEIGHT*(2/3)
    unlimited_mode_rect.x, unlimited_mode_rect.y = 3*fifth, HEIGHT*(2/3)

    # Rectangles
    rect1 = pygame.Rect([limited_mode_rect.x, limited_mode_rect.y, choice_w, choice_h])
    rect2 = pygame.Rect([unlimited_mode_rect.x, unlimited_mode_rect.y, choice_w, choice_h])

    # Draw rects & blit images
    screen.blit(limited_mode_img, (limited_mode_rect.x, limited_mode_rect.y))
    screen.blit(unlimited_mode_img, (unlimited_mode_rect.x, unlimited_mode_rect.y))
    pygame.draw.rect(screen, BLACK, rect1, width=1)
    pygame.draw.rect(screen, BLACK, rect2, width=1)

    # Flip
    pygame.display.flip()


def draw_losing():
    screen.fill(PSEUDO_BLACK)

    snake.draw_parameters(screen, WHITE)

    font = pygame.font.SysFont("comicsans", 80)
    youlose_font = font.render("You Lose", True, PSEUDO_WHITE)
    screen.blit(youlose_font, ((WIDTH-youlose_font.get_width())/2, HEIGHT/4))

    losing_snake_img = pygame.transform.scale(pygame.image.load("assets/snake_imgs/losing_snake.png"), (WIDTH/3, HEIGHT/3))
    screen.blit(losing_snake_img, ((WIDTH-losing_snake_img.get_width())/2, HEIGHT/4+youlose_font.get_height()))

    pygame.display.flip()


def check_collision(rect1, rect2):  # rect1 in rect2
    if rect2.x <= rect1.x < rect2.x + rect2.w:
        if rect2.y <= rect1.y < rect2.y + rect2.h:
            return True
    return False


def is_mouse_in_rect(mousex, mousey, rect):
    if rect.x <= mousex < rect.x + rect.w:
        if rect.y <= mousey < rect.y + rect.h:
            return True
    return False


# For not moving the snake in each frame, but less
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

snake = Snake()
fruits = [Fruit() for _ in range(2)]

fruit_types = {
    "apple": 1,
    "banana": 2,
    "pear": 3
}

# Main loop
is_started = False
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.set_direction("up")
            if event.key == pygame.K_DOWN:
                snake.set_direction("down")
            if event.key == pygame.K_RIGHT:
                snake.set_direction("right")
            if event.key == pygame.K_LEFT:
                snake.set_direction("left")

        if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if is_mouse_in_rect(mouse_x, mouse_y, limited_mode_rect):
                limited_mode, unlimited_mode = True, False
                is_started = True
            if is_mouse_in_rect(mouse_x, mouse_y, unlimited_mode_rect):
                limited_mode, unlimited_mode = False, True
                is_started = True

        if event.type == SCREEN_UPDATE and is_started:
            snake.move()

    if not is_started:
        draw_choice()
        continue

    # Check collision with fruit
    for fruit in fruits:
        if check_collision(snake.head, fruit.rect):
            # Add score in function of the type of the fruit
            snake.add_score(fruit_types[fruit.type])

            snake.add_length()
            fruit.spawn_fruit(snake.all)

    if snake.is_self_collision() and limited_mode:
        pygame.time.wait(2000)
        draw_losing()
        pygame.time.wait(2000)

        run = False
        pygame.quit()

    draw_screen()

# Done, Easily in about a week !!
