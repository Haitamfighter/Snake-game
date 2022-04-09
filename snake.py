import pygame

WIDTH, HEIGHT = 512, 512
cell_size = WIDTH//16


class Snake:
    def __init__(self):
        self.score = self.length = 0
        self.speed = cell_size

        self.width, self.height = cell_size, cell_size

        self.direction = "right"

        self.body = []
        self.head = pygame.Rect([0, 0, self.width, self.height])
        self.all = [self.head] + self.body

    def set_direction(self, direction):
        if direction == "up" and self.direction != "down":
            self.direction = "up"
        elif direction == "down" and self.direction != "up":
            self.direction = "down"
        elif direction == "right" and self.direction != "left":
            self.direction = "right"
        elif direction == "left" and self.direction != "right":
            self.direction = "left"

    def move_head(self):
        self.old_pos = self.head.topleft

        if self.direction == "up":
            self.head.y -= self.speed
        elif self.direction == "down":
            self.head.y += self.speed
        elif self.direction == "right":
            self.head.x += self.speed
        elif self.direction == "left":
            self.head.x -= self.speed

        if self.head.x < 0:
            self.head.x = WIDTH
        elif self.head.x > WIDTH:
            self.head.x = 0
        if self.head.y < 0:
            self.head.y = HEIGHT
        elif self.head.y > HEIGHT:
            self.head.y = 0

    def move(self):
        self.move_head()

        # My own wonderful reversed logic LOL SO JOYFUL I MADE THE SNAKE GROW !!!
        copy_body = self.body[:]
        for index in range(len(self.body)-1, -1, -1):
            rect = self.body[index]
            if index == 0:
                rect.x = self.old_pos[0]
                rect.y = self.old_pos[1]
            else:
                rect.x = self.body[index-1].x
                rect.y = self.body[index-1].y
            copy_body[index] = rect
        self.body = copy_body[:]
        self.all = [self.head] + self.body

    def is_self_collision(self):
        for body in self.body:
            if body.x == self.head.x and body.y == self.head.y:
                return True
        return False

    def add_score(self, amount: int):
        self.score += amount

    def add_length(self):
        self.body.append(pygame.Rect([self.body[-1].x if len(self.body) != 0 else self.old_pos[0],
                                      self.body[-1].y if len(self.body) != 0 else self.old_pos[1],
                                      self.width, self.height]))
        self.all = [self.head] + self.body
        self.length += 1

    def draw_parameters(self, surface, color):
        font = pygame.font.SysFont("comicsans", 20)

        # Length
        txt_font = font.render(f"length: {self.length}", True, color)
        surface.blit(txt_font, (0, 0))

        # Score
        txt_font = font.render(f"score: {self.score}", True, color)
        surface.blit(txt_font, (WIDTH-txt_font.get_width()-10, 0))

    def draw(self, surface, color):
        for i in self.body:
            pygame.draw.rect(surface, color, i)

        head_color = tuple(abs(100-color[i]) for i in range(3))
        pygame.draw.rect(surface, head_color, self.head)

        self.draw_parameters(surface, tuple(color[i]-60 for i in range(3)))
