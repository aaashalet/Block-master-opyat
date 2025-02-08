import pygame


def show_menu(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    title_text = font.render("Block Master", True, (255, 255, 255))
    start_text = font.render("Играть", True, (0, 255, 0))

    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    start_rect = start_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    waiting = False
