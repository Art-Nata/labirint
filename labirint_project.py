import argparse
import sys

import pygame

WIND0W_SIZE = WINDOW_WIDTH, WINDOW_HEIGTH = 600, 600

FPS = 40
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
        self.delay = 300
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


def message_show(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, 1, (100, 255, 100))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGTH // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    pygame.draw.rect(screen, (10, 100, 10), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def load_image(name, color_key=None):
    try:
        image = pygame.image.load(f'images/{name}').convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Приветствую тебя, герой!", "",
                  "Помоги малышу-огню!",
                  "Выведи его из лабиринта и спаси от",
                  "супер-пупер Al",
                  "", "Удачи!"]

    screen = pygame.display.set_mode(WIND0W_SIZE)
    clock1 = pygame.time.Clock()
    fon = pygame.transform.scale(load_image('fon.png'), WIND0W_SIZE)
    screen.blit(fon, (0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 40)
    text_coord = 80
    for line in intro_text:
        string_rendered = font.render(line, 1, (70, 50, 110))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 40
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock1.tick(FPS)


def main():
    start_screen()
    pygame.init()
    screen = pygame.display.set_mode(WIND0W_SIZE)

    for lvl in range(1, 2):
        print(lvl)
        map_file = "map%s" % lvl
        labirint = Labirint(map_file, [0, 2], 2)
        hero = Hero('hero.png', (1, 1))
        enemy = Enemy('enemy.png', (7, 7))
        game = Game(labirint, hero, enemy)

        running = True
        game_over = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == ENEMY_EVENT_TYPE and not game_over:
                    game.move_enemy()
            if not game_over:
                game.update_hero()
            screen.fill((0, 0, 0))
            game.render(screen)
            if game.check_rout():
                game_over = True
                message_show(screen, 'Увы! Al победил')
            if game.check_next_level():
                message_show(screen, 'Вы спасены!')
                game_over = True
            pygame.display.flip()
            clock.tick(FPS)

    terminate()


if __name__ == '__main__':
    main()
