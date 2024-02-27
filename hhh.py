def main():
    pygame.init() # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Super Mario Boy") # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT)) # Создание видимой поверхности
    # будем использовать как фон

    renderer = helperspygame.RendererPygame() # визуализатор
    for lvl in range(1,4):
        loadLevel("levels/map_%s" % lvl)
        bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

        left = right = False # по умолчанию - стоим
        up = False
        running = False
        try:
            hero = Player(playerX, playerY) # создаем героя по (x,y) координатам
            entities.add(hero)
        except:
            print (u"Не удалось на карте найти героя, взяты координаты по-умолчанию")
            hero = Player(65, 65)
        entities.add(hero)

        timer = pygame.time.Clock()

        camera = Camera(camera_configure, total_level_width, total_level_height)

        while not hero.winner: # Основной цикл программы
            timer.tick(60)
            for e in pygame.event.get(): # Обрабатываем события
                if e.type == QUIT:
                    raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_LSHIFT:
                    running = True

                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_LSHIFT:
                    running = False
            for sprite_layer in sprite_layers: # перебираем все слои
                if not sprite_layer.is_object_group: # и если это не слой объектов
                   renderer.render_layer(screen, sprite_layer) # отображаем его

            for e in entities:
                screen.blit(e.image, camera.apply(e))
            animatedEntities.update() # показываеaм анимацию
            monsters.update(platforms) # передвигаем всех монстров
            camera.update(hero) # центризируем камеру относительно персонаж
            center_offset = camera.reverse(CENTER_OF_SCREEN)
            renderer.set_camera_position_and_size(center_offset[0], center_offset[1], \
                                                  WIN_WIDTH, WIN_HEIGHT, "center")
            hero.update(left, right, up, running, platforms) # передвижение
            pygame.display.update()     # обновление и вывод всех изменений на экран
            screen.blit(bg, (0, 0))      # Каждую итерацию необходимо всё перерисовывать
        for sprite_layer in sprite_layers:
            if not sprite_layer.is_object_group:
                renderer.render_layer(screen, sprite_layer)
        # когда заканчиваем уровень
        for e in entities:
            screen.blit(e.image, camera.apply(e)) # еще раз все перерисовываем
        font=pygame.font.Font(None,38)
        text=font.render(("Thank you MarioBoy! but our princess is in another level!"), 1,(255,255,255))# выводим надпись
        screen.blit(text, (10,100))
        pygame.display.update()
        time.wait(10000) # ждем 10 секунд и после - переходим на следующий уровень