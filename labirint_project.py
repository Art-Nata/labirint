
import sys

import pygame
from pygame import time

from date.libs import load_image, terminate, message_show, saved_name
from date.window_end import end_screen
from date.window_start import start_screen

WIND0W_SIZE = WINDOW_WIDTH, WINDOW_HEIGTH = 600, 600

FPS = 50
MAPS_DIR = 'Maps'
TILE_SIZE = 40
ENEMY_EVENT_TYPE = 40

map_file = None
clock = pygame.time.Clock()


class Labirint:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f'{MAPS_DIR}/{filename}.txt') as open_file:
            for line in open_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        tile_image = {0: 'road.png', 1: 'wall.png', 2: 'end.png'}
        for x in range(self.height):
            for y in range(self.width):
                self.image = load_image(tile_image[self.get_tile_id((x, y))])
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                screen.blit(self.image, rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def find_step(self, start_p, end_p):
        INF = 1000
        x, y = start_p
        distance = [[INF] * self.width for _ in range(self.height)]
        distance[y][x] = 0
        pred = [[None] * self.width for _ in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for d_x, d_y in (0, 1), (1, 0), (-1, 0), (0, -1):
                new_x, new_y = x + d_x, y + d_y
                if 0 <= new_x < self.width and 0 < new_y < self.height and \
                        self.is_free((new_x, new_y)) and distance[new_y][new_x] == INF:
                    distance[new_y][new_x] = distance[y][x] + 1
                    pred[new_y][new_x] = (x, y)
                    queue.append((new_x, new_y))
        x, y = end_p
        if start_p == end_p or distance[y][x] == INF:
            return start_p
        while pred[y][x] != start_p:
            x, y = pred[y][x]
        return x, y


class Hero:

    def __init__(self, file_img, position):
        self.x, self.y = position
        self.image = load_image(file_img, -1)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE - 1, TILE_SIZE - 1))

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        d = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - d, self.y * TILE_SIZE - d))


class Enemy:

    def __init__(self, file_img, position):
        self.x, self.y = position
        self.delay = 400
        pygame.time.set_timer(ENEMY_EVENT_TYPE, self.delay)
        self.image = load_image(file_img, -1)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE - 1, TILE_SIZE - 1))

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        d = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - d, self.y * TILE_SIZE - d))


class Game:
    def __init__(self, labirint, hero, enemy):
        self.labirint = labirint
        self.hero = hero
        self.enemy = enemy

    def render(self, screen):
        self.labirint.render(screen)
        self.hero.render(screen)
        self.enemy.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.labirint.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def move_enemy(self):
        position = self.labirint.find_step(self.enemy.get_position(), self.hero.get_position())
        self.enemy.set_position(position)

    def check_next_level(self):
        return self.labirint.get_tile_id(self.hero.get_position()) == self.labirint.finish_tile

    def check_rout(self):
        return self.hero.get_position() == self.enemy.get_position()


pygame.init()
screen = pygame.display.set_mode(WIND0W_SIZE)
#Создаём список уровней
LEVELS = [
    {
     "enemy": Enemy('enemy.png', (7, 7)),
     "hero": Hero('hero.png', (1, 1)),
     "labirint": Labirint('map1', [0, 2], 2)
     },
    {"hero": Hero('hero.png', (7, 14)),
     "enemy": Enemy('enemy.png', (1, 1)),
     "labirint": Labirint('map2', [0, 2], 2)
     },
     {
     "enemy": Enemy('enemy.png', (11, 7)),
     "hero": Hero('hero.png', (4, 11)),
     "labirint": Labirint('map3', [0, 2], 2)
     }
]

name_player = start_screen(WIND0W_SIZE)


end_game_viv = True
for lvl in range(len(LEVELS)):
    labirint = LEVELS[lvl]['labirint']
    hero = LEVELS[lvl]['hero']
    enemy = LEVELS[lvl]['enemy']
    game = Game(labirint, hero, enemy)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == ENEMY_EVENT_TYPE:
                game.move_enemy()
            elif event.type == pygame.KEYDOWN:
                game.update_hero()
        if game.check_rout():
            end_game_viv = False
            running = False
        elif game.check_next_level():
            running = False

        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

end_screen(end_game_viv, name_player, WIND0W_SIZE)
