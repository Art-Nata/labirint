import pygame
from pygame import time

from date.libs import load_image, load_sound


def start_screen(window_size):
    # имя игрока
    name_hero = ""
    # флаг окончания набора имени
    saved = False
    # текст, который появляется после набора имени игрока
    intro_text = ["Помоги малышу-огню!",
                  "Выведи его из лабиринта и спаси от",
                  "супер-пупер Al",
                  "", "Удачи!",
                  ""]
    load_sound('start.mp3')
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

        #отображение введённого имени игрока
        text_input = font.render(name_hero, True, (0, 0, 0))
        text_input_rect = text_input.get_rect(center=(300, 200))
        screen.blit(text_input, text_input_rect)
        pygame.draw.line(screen, (0, 0, 0), (150, 210), (450, 210), 2)

        if saved:
            line = 250
            for text_list in intro_text:
                font1 = pygame.font.Font(None, 36)
                text1 = font1.render(text_list, 1, (0, 0, 0))
                intro_rect = text1.get_rect(center=(300, line))
                screen.blit(text1, intro_rect)
                line += 50
            font1 = pygame.font.Font(None, 24)
            text1 = font1.render("Для продолжения нажми любую клавишу", 1, (0, 0, 0))
            intro_rect = text1.get_rect(center=(300, line))
            screen.blit(text1, intro_rect)

        pygame.display.flip()
