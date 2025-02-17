import pygame


def show_game_over_screen(screen, score):
    pygame.font.init()
    font_large = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    screen.fill((30, 30, 30))
    text_game_over = font_large.render("Ты проиграл!", True, (255, 0, 0))
    text_score = font_small.render(f"Очки: {score}", True, (255, 255, 255))

    button_text = font_small.render("Сыграть снова!", True, (0, 0, 0))
    button_w, button_h = 220, 60
    button_x = (screen.get_width() - button_w) // 2
    button_y = (screen.get_height() - button_h) // 2 + 50
    button_rect = pygame.Rect(button_x, button_y, button_w, button_h)

    running = True
    while running:
        screen.fill((30, 30, 30))
        screen.blit(text_game_over, ((screen.get_width() - text_game_over.get_width()) // 2, 150))
        screen.blit(text_score, ((screen.get_width() - text_score.get_width()) // 2, 220))

        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        screen.blit(button_text, (
        button_x + (button_w - button_text.get_width()) // 2, button_y + (button_h - button_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

    return False
