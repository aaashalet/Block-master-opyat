import pygame
from shapes import get_random_shape

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Master")

GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
GRID_COLOR = (50, 50, 50)

game_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

current_shape = get_random_shape()

selected_shape = None
shape_x, shape_y = 100, 100
dragging = False


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_shape(shape, pos_x, pos_y):
    block_color = (75, 0, 130)
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                x = pos_x + col_idx * CELL_SIZE
                y = pos_y + row_idx * CELL_SIZE
                pygame.draw.rect(screen, block_color, (x, y, CELL_SIZE, CELL_SIZE))


def draw_board():
    block_color = (25, 25, 112)
    for row_idx, row in enumerate(game_board):
        for col_idx, cell in enumerate(row):
            if cell:
                x = col_idx * CELL_SIZE
                y = row_idx * CELL_SIZE
                pygame.draw.rect(screen, block_color, (x, y, CELL_SIZE, CELL_SIZE))


def clear_full_lines_and_columns():
    global game_board

    # Очищаем полностью заполненные строки
    for row_idx in range(GRID_SIZE):
        if all(game_board[row_idx]):
            game_board[row_idx] = [0] * GRID_SIZE

    # Очищаем полностью заполненные столбцы
    for col_idx in range(GRID_SIZE):
        if all(game_board[row][col_idx] for row in range(GRID_SIZE)):
            for row in range(GRID_SIZE):
                game_board[row][col_idx] = 0


def can_place_shape(shape, grid_x, grid_y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board_x = grid_x + col_idx
                board_y = grid_y + row_idx
                if board_x >= GRID_SIZE or board_y >= GRID_SIZE or game_board[board_y][board_x] == 1:
                    return False
    return True


def can_place_anywhere(shape):
    for grid_y in range(GRID_SIZE):
        for grid_x in range(GRID_SIZE):
            if can_place_shape(shape, grid_x, grid_y):
                return True
    return False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for row_idx, row in enumerate(current_shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        block_x = shape_x + col_idx * CELL_SIZE
                        block_y = shape_y + row_idx * CELL_SIZE
                        block_rect = pygame.Rect(block_x, block_y, CELL_SIZE, CELL_SIZE)
                        if block_rect.collidepoint(mouse_x, mouse_y):
                            dragging = True
                            selected_shape = current_shape

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            shape_x = mouse_x - (CELL_SIZE // 2)
            shape_y = mouse_y - (CELL_SIZE // 2)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            shape_x = round(shape_x / CELL_SIZE) * CELL_SIZE
            shape_y = round(shape_y / CELL_SIZE) * CELL_SIZE

            grid_x, grid_y = shape_x // CELL_SIZE, shape_y // CELL_SIZE

            if can_place_shape(current_shape, grid_x, grid_y):
                for row_idx, row in enumerate(current_shape):
                    for col_idx, cell in enumerate(row):
                        if cell:
                            game_board[grid_y + row_idx][grid_x + col_idx] = 1

                clear_full_lines_and_columns()

                if not can_place_anywhere(current_shape):
                    print("Игра окончена!")
                    running = False
                else:
                    current_shape = get_random_shape()
                    shape_x, shape_y = 100, 100

    screen.fill((0, 0, 0))

    draw_grid()
    draw_board()
    draw_shape(current_shape, shape_x, shape_y)

    pygame.display.flip()

pygame.quit()
