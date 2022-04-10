import random
import os
from pytimedinput import timedInput
from colorama import Fore, init
init(autoreset=True)


# Width + Height
width, height = 40, 16

# The list that'll be the most important part of this project
field_list = [[' ' for i in range(width)] for j in range(height)]


# Classes
class SnakePart:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.head_x = self.head_y = 0
        self.direction = 'd'

        self.body = []

    def move(self, key=None):
        keys_dict = {
            'w': (0, -1),
            'a': (-1, 0),
            's': (0, 1),
            'd': (1, 0)
        }

        if key is None:
            key = self.direction

        if (self.direction == 'w' and key != 's') or (self.direction == 's' and key != 'w') or\
                (self.direction == 'a' and key != 'd') or (self.direction == 'd' and key != 'a'):
            self.direction = key
        else:
            key = self.direction

        self.old_pos = (self.head_x, self.head_y)

        self.head_x += keys_dict[key][0]
        self.head_y += keys_dict[key][1]

        if self.head_x == width:
            self.head_x = 0
        if self.head_y == height:
            self.head_y = 0
        if self.head_x == -1:
            self.head_x = width - 1
        if self.head_y == -1:
            self.head_y = height - 1

        self.move_parts()

    def add_part(self):
        if not self.body:
            self.body.append(SnakePart(self.old_pos[0], self.old_pos[1]))
        else:
            self.body.append(SnakePart(self.body[-1].x, self.body[-1].y))

    def move_parts(self):
        # Another Victory for the Amazing Unbelievable Coder's Talent
        body_copy = list(reversed(self.body))
        for num, part in enumerate(list(reversed(self.body))):
            if num == len(self.body)-1:
                part.x, part.y = self.old_pos
            else:
                part.x, part.y = list(reversed(self.body))[num+1].x, list(reversed(self.body))[num+1].y
            body_copy[num] = part
        self.body = list(reversed(body_copy))


class Fruit:
    def __init__(self):
        self.random_pos()

    def random_pos(self):
        self.x = random.randrange(0, width)
        self.y = random.randrange(0, height)


# Draw the field: str
def draw_field():
    for _ in range(width+2):
        if _ != width+1:
            print(Fore.CYAN + '#', end='')
        else:
            print(Fore.CYAN + '#')

    for j in field_list:
        print(Fore.CYAN + '#', end='')
        for i in j:
            if i == 'H':
                print(Fore.YELLOW + 'H', end='')
            elif i == 'X':
                print(Fore.GREEN + 'X', end='')
            elif i == 'A':
                print(Fore.RED + 'A', end='')
            else:
                print(' ', end='')
        print(Fore.CYAN + '#')

    for _ in range(width+2):
        if _ != width+1:
            print(Fore.CYAN + '#', end='')
        else:
            print(Fore.CYAN + '#')


# Instance
snake = Snake()
fruit = Fruit()

print("HI, This is the normal form of the snake game!\nUse WASD to move your snake")
print("Remember to use a proper terminal such as 'CMD' and sorry for the glitches.. Enjoy!")
while True:
    os.system("cls")
    draw_field()

    txt, _ = timedInput('', timeout=0.01)

    field_list = [[' ' for i in range(width)] for j in range(height)]

    # Spawn fruit
    field_list[fruit.y][fruit.x] = 'A'

    if txt in ['w', 'a', 's', 'd']:
        snake.move(key=txt)
    else:
        snake.move()

    for body_part in snake.body:
        field_list[body_part.y][body_part.x] = 'X'
    field_list[snake.head_y][snake.head_x] = 'H'

    # Check for collision
    if snake.head_x == fruit.x and snake.head_y == fruit.y:
        fruit.random_pos()
        snake.add_part()
