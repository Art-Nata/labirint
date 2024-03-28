import pygame
from pygame import time

from date.game_classes import Labirint, Hero, Enemy, Game
from date.libs import terminate, saved_name
from date.window_end import end_screen
from date.window_start import start_screen

from date import (WIND0W_SIZE, FPS, ENEMY_EVENT_TYPE)


map_file = None

pygame.init()
screen = pygame.display.set_mode(WIND0W_SIZE)
clock = pygame.time.Clock()
delay = 400


# запускаем начальное окно, где получаем имя(ник) игрока и возвращаем его в переменную
name_player = start_screen(WIND0W_SIZE)
game_over = False  #флаг окончания игры
pygame.time.set_timer(ENEMY_EVENT_TYPE, delay)

while not game_over:
    # Создаём список уровней, можно расширять по желанию
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

    # флаг победы в игре
    end_game_viv = True
    for lvl in range(len(LEVELS)):
        labirint = LEVELS[lvl]['labirint']
        hero = LEVELS[lvl]['hero']

        enemy = LEVELS[lvl]['enemy']
        game = Game(labirint, hero, enemy)
        if not end_game_viv:
            break
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
        time.wait(2000)

    # запускаем финальное окно, передаём имя игрока, флаг победы в игре и размеры окна
    game_over = end_screen(end_game_viv, name_player)
