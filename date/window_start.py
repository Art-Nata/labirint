import pygame
from pygame import time

from date.libs import load_image


def start_screen(window_size):
    name_hero = ""
    saved = False

    screen = pygame.display.set_mode(window_size)
    fon = pygame.transform.scale(load_image('fon.png'), window_size)
    screen.blit(fon, (0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 40)

    text = font.render("Приветствую тебя, о герой!", 1, (0, 0, 0))
    intro_rect = text.get_rect(center=(300, 100))
    screen.blit(text, intro_rect)

    text = font.render("Представься", 1, (0, 0, 0))
    intro_rect = text.get_rect(center=(300, 150))
    screen.blit(text, intro_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not saved:
                    if event.key == pygame.K_RETURN:
                        saved = True
                    elif event.key == pygame.K_BACKSPACE:
                        name_hero = name_hero[:-1]
                    else:
                        name_hero += event.unicode
                else:
                    time.wait(3000)
                    return name_hero
            elif event.type == pygame.MOUSEBUTTONDOWN and saved:
                time.wait(3000)
                return name_hero

        fon = pygame.transform.scale(load_image('fon.png'), window_size)
        screen.blit(fon, (0, 0))
        pygame.font.init()
        font = pygame.font.Font(None, 40)
        text = font.render("Приветствую тебя, о герой!", 1, (0, 0, 0))
        intro_rect = text.get_rect(center=(300, 100))
        screen.blit(text, intro_rect)

        text = font.render("Представься", 1, (0, 0, 0))
        intro_rect = text.get_rect(center=(300, 150))
        screen.blit(text, intro_rect)
        text_input = font.render(name_hero, True, (0, 0, 0))
        text_input_rect = text_input.get_rect(center=(300, 200))
        screen.blit(text_input, text_input_rect)
        pygame.draw.line(screen, (0, 0, 0), (150, 210), (450, 210), 2)

        if saved:
            font1 = pygame.font.Font(None, 36)
            text1 = font1.render("Помоги мальнькому живому Огоньку", 1, (0, 0, 0))
            intro_rect = text1.get_rect(center=(300, 250))
            screen.blit(text1, intro_rect)
            text1 = font1.render("выбраться из лабиринта ", 1, (0, 0, 0))
            intro_rect = text1.get_rect(center=(300, 300))
            screen.blit(text1, intro_rect)
            text1 = font1.render("и спастись от бездушного AI ", 1, (0, 0, 0))
            intro_rect = text1.get_rect(center=(300, 350))
            screen.blit(text1, intro_rect)

        pygame.display.flip()

