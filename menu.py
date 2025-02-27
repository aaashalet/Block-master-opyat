import pygame
import random

settings = {
    "volume": 1.0,
    "effects": True,
    "random_colors": False,
    "selected_color": (75, 0, 130)
}


def show_menu(screen):
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        title_text = font.render("Block Master", True, (255, 255, 255))
        start_text = font.render("Играть", True, (0, 255, 0))
        settings_text = font.render("Настройки", True, (0, 255, 255))

        title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
        start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        settings_rect = settings_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))

        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(settings_text, settings_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return
                elif settings_rect.collidepoint(event.pos):
                    show_settings(screen)
                    break


def show_settings(screen):
    while True:
        screen.fill((50, 50, 50))
        font = pygame.font.Font(None, 50)
        back_text = font.render("Назад", True, (255, 0, 0))
        back_rect = back_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))

        effects_text = font.render(f"Звуковые эффекты: {'Вкл' if settings['effects'] else 'Выкл'}", True,
                                   (255, 255, 255))
        effects_rect = effects_text.get_rect(center=(screen.get_width() // 2, 200))

        color_text = font.render(f"Случайные цвета(оно не работает(((): {'Вкл' if settings['random_colors'] else 'Выкл'}", True,
                                 (255, 255, 255))
        color_rect = color_text.get_rect(center=(screen.get_width() // 2, 300))

        choose_color_text = font.render("Выбор цвета(не работает))", True, settings['selected_color'])
        choose_color_rect = choose_color_text.get_rect(center=(screen.get_width() // 2, 400))

        screen.blit(back_text, back_rect)
        screen.blit(effects_text, effects_rect)
        screen.blit(color_text, color_rect)
        screen.blit(choose_color_text, choose_color_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                elif effects_rect.collidepoint(event.pos):
                    settings['effects'] = not settings['effects']
                elif color_rect.collidepoint(event.pos):
                    settings['random_colors'] = not settings['random_colors']
                elif choose_color_rect.collidepoint(event.pos):
                    settings['selected_color'] = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])

        pygame.time.delay(100)
