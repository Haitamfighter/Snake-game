import pygame
import random

WIDTH, HEIGHT = 512, 512
cell_size = WIDTH//16


class Fruit:
    def __init__(self):
        self.spawn_fruit([])

    def random_position(self, snake_all_list: list):
        possible_x = [_ for _ in range(self.rect.w, WIDTH) if _ % (WIDTH//16) == 0]
        possible_y = [_ for _ in range(self.rect.h, HEIGHT) if _ % (HEIGHT//16) == 0]
        while True:
            empty = True
            self.rect.x = random.choice(possible_x) - self.rect.w
            self.rect.y = random.choice(possible_y) - self.rect.h
            for rect in snake_all_list:
                if self.rect.x == rect.x and self.rect.y == rect.y:
                    empty = False
            if empty:
                break

    def random_fruit(self):
        images = ["apple.png", "banana.png", "pear.png"]
        rand_image = random.choice(images)
        self.image = pygame.transform.scale(pygame.image.load(f"assets/fruit_imgs/{rand_image}"),
                                            (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.type = rand_image.split('.')[0]

    def spawn_fruit(self, snake_all_list: list):
        self.random_fruit()
        self.random_position(snake_all_list)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
