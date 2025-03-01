import pygame
import random
import settings


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

        effects_text = font.render(f"Звуковые эффекты: {'Вкл' if settings.config['effects'] else 'Выкл'}", True,
                                   (255, 255, 255))
        effects_rect = effects_text.get_rect(center=(screen.get_width() // 2, 200))

        music_text = font.render(f"Музыка: {'Вкл' if settings.config['music'] else 'Выкл'}", True, (255, 255, 255))
        music_rect = music_text.get_rect(center=(screen.get_width() // 2, 300))

        screen.blit(back_text, back_rect)
        screen.blit(effects_text, effects_rect)
        screen.blit(music_text, music_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                elif effects_rect.collidepoint(event.pos):
                    settings.config['effects'] = not settings.config['effects']
                elif music_rect.collidepoint(event.pos):
                    settings.config['music'] = not settings.config['music']
                    settings.apply_settings()

        pygame.time.delay(100)