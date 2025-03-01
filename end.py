import pygame


def show_game_over_screen(screen, score):
    screen.fill((0, 0, 0))  # Черный фон
    font = pygame.font.Font(None, 72)
    text = font.render("Ты проиграл", True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))

    score_font = pygame.font.Font(None, 50)
    score_text = score_font.render(f"Очки: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)

    pygame.display.flip()

    pygame.time.delay(3000)  
