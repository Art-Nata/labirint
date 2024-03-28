import pygame
from pygame import time

from date.libs import saved_name, load_image, load_list, terminate
from date import (WIND0W_SIZE)


def end_screen(end_game, name):
    list_heroes = load_list('rez.txt')

    if end_game:
        list_end_game = [f"{name}, ты справился!",
                         "Огонь вырвался из лабиринта",
                         "и принесёт свет и тепло людям.",
                         "Твоё имя внесено в Книгу ГЕРОЕВ",
                         "",
                         f"1. {name}"]
        for i in range(len(list_heroes)):
            list_end_game.append(f'{i + 2}. {list_heroes[i]}')
        saved_name(name)
    else:
        list_end_game = [f"{name}, не переживай!",
                         "Пробуй и обязательно победишь!",
                         "Книга ГЕРОЕВ ждёт тебя",
                         ""]

    screen = pygame.display.set_mode(WIND0W_SIZE)
    fon = pygame.transform.scale(load_image('fon.png'), WIND0W_SIZE)
    screen.blit(fon, (0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 40)

    for i in range(len(list_end_game)):
        text = font.render(list_end_game[i], 1, (0, 0, 0))
        intro_rect = text.get_rect(center=(300, 100 + 50 * i))
        screen.blit(text, intro_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Поиграем ещё?        (Y / N)", 1, (0, 0, 0))
    intro_rect = text.get_rect(center=(300, 500))
    screen.blit(text, intro_rect)

    game_over = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    game_over = False
                    running = False
                elif event.key == pygame.K_n:
                    terminate()
        fon = pygame.transform.scale(load_image('fon.png'), WIND0W_SIZE)
        screen.blit(fon, (0, 0))
        pygame.font.init()
        font = pygame.font.Font(None, 40)
        for i in range(len(list_end_game)):
            text = font.render(list_end_game[i], 1, (0, 0, 0))
            intro_rect = text.get_rect(center=(300, 100 + 50 * i))
            screen.blit(text, intro_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Поиграем ещё?        (Y / N)", 1, (0, 0, 0))
        intro_rect = text.get_rect(center=(300, 500))
        screen.blit(text, intro_rect)

        pygame.display.flip()
    time.wait(3000)

    return game_over
