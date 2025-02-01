import pygame
from shapes import get_random_shape

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Master")

GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
GRID_COLOR = (50, 50, 50)

current_shape = get_random_shape()


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_shape(shape, pos_x, pos_y):
    block_color = (0, 200, 255)
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                x = pos_x + col_idx * CELL_SIZE
                y = pos_y + row_idx * CELL_SIZE
                pygame.draw.rect(screen, block_color, (x, y, CELL_SIZE, CELL_SIZE))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    draw_grid()

    draw_shape(current_shape, 100, 100)

    pygame.display.flip()

pygame.quit()
