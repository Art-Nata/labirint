import os
import sys

import pygame


def message_show(screen, message):
    font2 = pygame.font.Font(None, 50)
    text2 = font2.render(message, 1, (100, 255, 100))
    text_rect = text2.get_rect(center=(300, 100))

    screen.blit(text2, text_rect)


def load_image(name, color_key=None):
    try:
        img_dir = os.path.abspath('images')
        image = pygame.image.load(os.path.join(img_dir, name)).convert()
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


def saved_name(name):
    with open('rez.txt', 'a', encoding='utf-8') as f:
        f.writelines(name+'\n')


def load_list(file):
    list_heroes = open(file, 'r', encoding='utf_8').readlines()
    if len(list_heroes) > 3:
        return list_heroes[:3]
    else:
        return list_heroes[:len(list_heroes)]