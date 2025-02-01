import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Master")

running = True

GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
GRID_COLOR = (50, 50, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    pygame.display.flip()

pygame.quit()
