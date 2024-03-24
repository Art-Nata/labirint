import pygame

from date.libs import saved_name, load_image, load_list, terminate


def end_screen(end_game, name, window_size):
    print("kkkk")
    list_heroes = load_list('rez.txt')

    if end_game:
        list_end_game = [f"{name}, ты справился!",
                         "Огонь вырвался из лабиринта",
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
        for i in range(len(list_heroes)):
            list_end_game.append(f'{i + 1}. {list_heroes[i]}')

    screen = pygame.display.set_mode(window_size)
    fon = pygame.transform.scale(load_image('fon.png'), window_size)
    screen.blit(fon, (0, 0))
    pygame.font.init()
    font = pygame.font.Font(None, 40)

    for i in range(len(list_end_game)):
        text = font.render(list_end_game[i], 1, (0, 0, 0))
        intro_rect = text.get_rect(center=(300, 100 + 50 * i))
        screen.blit(text, intro_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        fon = pygame.transform.scale(load_image('fon.png'), window_size)
        screen.blit(fon, (0, 0))
        pygame.font.init()
        font = pygame.font.Font(None, 40)
        for i in range(len(list_end_game)):
            text = font.render(list_end_game[i], 1, (0, 0, 0))
            intro_rect = text.get_rect(center=(300, 100 + 50 * i))
            screen.blit(text, intro_rect)

        pygame.display.flip()
