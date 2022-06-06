"""
Author: Fran Moreno
Contact: fran.moreno.se@gmail.com
Date: 05/06/2022

Desc: 
# Fill 
"""
import pygame
import random
from dataclasses import dataclass
from enum import Enum

GAME_WIDTH, GAME_HEIGHT = 20, 20


@dataclass
class Point:
    x: int
    y: int


class Difficulty(Enum):
    Easy = 5
    Medium = 10
    Hard = 20
    Insane = 30


class Apple:
    def __init__(self, tail):
        self.color = (255, 0, 0)
        self.x = None
        self.y = None
        self.new(tail)

    def new(self, tail):
        while True:
            self.x = random.randint(0, GAME_WIDTH - 1)
            self.y = random.randint(0, GAME_HEIGHT - 1)
            if Point(self.x, self.y) not in tail:
                break


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dir = 'd'
        self.color = (255, 255, 255)
        self.tail = [Point(self.x, self.y)]

    def update(self, apple):
        self._move()
        if self._collision():
            return True
        self._check_boundaries()
        self._found_apple(apple)
        return False

    def _move(self):
        if self.dir == 'u':
            self.y -= 1
        elif self.dir == 'd':
            self.y += 1
        elif self.dir == 'l':
            self.x -= 1
        elif self.dir == 'r':
            self.x += 1

    def _check_boundaries(self):
        if (self.x >= GAME_WIDTH) and (self.dir == 'r'):
            self.x = 0
        elif (self.x < 0) and (self.dir == 'l'):
            self.x = GAME_WIDTH - 1
        elif (self.y >= GAME_HEIGHT) and (self.dir == 'd'):
            self.y = 0
        elif (self.y < 0) and (self.dir == 'u'):
            self.y = GAME_HEIGHT - 1

    def _collision(self):
        if Point(self.x, self.y) in self.tail:
            return True
        return False

    def _found_apple(self, apple: Apple):
        if (self.x == apple.x) and (self.y == apple.y):
            self.tail.insert(0, Point(apple.x, apple.y))
            apple.new(self.tail)
        else:
            self.tail.insert(0, Point(self.x, self.y))
            self.tail.pop()


class Canvas:
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.color = (0, 0, 0)
        self.scale = 20
        self.block_size = 18
        self.canvas = pygame.display.set_mode((self.game_width * self.scale, self.game_height * self.scale))
        pygame.display.set_caption("Snake Game")
        pygame.display.flip()

        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.screen = pygame.Surface((self.game_width * self.scale, self.game_height * self.scale))

    def update(self, snake: Snake, apple: Apple):
        self.screen.fill(self.color)
        self._draw_snake(snake)
        self._draw_apple(apple)
        text = self.font.render(f'score: {len(snake.tail)-1}', True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.center = (18 * self.scale, 1 * self.scale)
        self.canvas.blit(pygame.transform.scale(self.screen, self.canvas.get_rect().size), (0, 0))
        self.canvas.blit(text, textRect)

    def _draw_snake(self, snake: Snake):
        for point in snake.tail:
            pygame.draw.rect(self.screen, snake.color,
                             (point.x * self.scale, point.y * self.scale, self.block_size, self.block_size),
                             border_radius=10)

    def _draw_apple(self, apple: Apple):
        pygame.draw.rect(self.screen, apple.color,
                         (apple.x * self.scale, apple.y * self.scale, self.block_size, self.block_size),
                         border_radius=7)


class Game:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.speed = difficulty.value
        self.clock = pygame.time.Clock()
        self.running = False
        self.pause = False
        self.score = 0

        pygame.init()
        self.canvas = Canvas(self.width, self.height)
        self.snake = Snake(int(self.width/2), int(self.height/2))
        self.apple = Apple(self.snake.tail)

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(self.speed)
            self._get_inputs()

            collision = self.snake.update(self.apple)
            if collision:
                break
            self.score = len(self.snake.tail) - 1
            self.canvas.update(self.snake, self.apple)
            pygame.display.update()
        pygame.quit()

    def _get_inputs(self):
        change_to = self.snake.dir
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.pause = True

                elif (event.key == pygame.K_UP) and (self.snake.dir != 'd'):
                    change_to = 'u'
                elif (event.key == pygame.K_DOWN) and (self.snake.dir != 'u'):
                    change_to = 'd'
                elif (event.key == pygame.K_LEFT) and (self.snake.dir != 'r'):
                    change_to = 'l'
                elif (event.key == pygame.K_RIGHT) and (self.snake.dir != 'l'):
                    change_to = 'r'

        if change_to == 'u' and self.snake.dir != 'd':
            self.snake.dir = change_to
        elif change_to == 'd' and self.snake.dir != 'u':
            self.snake.dir = change_to
        elif change_to == 'l' and self.snake.dir != 'r':
            self.snake.dir = change_to
        elif change_to == 'r' and self.snake.dir != 'l':
            self.snake.dir = change_to


if __name__ == '__main__':
    game = Game(GAME_WIDTH, GAME_HEIGHT, Difficulty.Easy)
    game.run()


