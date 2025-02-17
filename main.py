import pygame
import random
import menu
import game_over
from shapes import get_random_shape, get_helpful_shape

pygame.init()

WIDTH, HEIGHT = 600, 700
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
BOTTOM_PANEL_HEIGHT = 100
GRID_COLOR = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Master")

game_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0

def generate_shapes():
    return [get_random_shape() if random.random() > 0.2 else get_helpful_shape(game_board) for _ in range(3)]

current_shapes = generate_shapes()
shape_positions = [(100, 620), (250, 620), (400, 620)]
placed_shapes = [False, False, False]
selected_shape = None
dragging = False

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT - BOTTOM_PANEL_HEIGHT))
    for y in range(0, HEIGHT - BOTTOM_PANEL_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_board():
    block_color = (25, 25, 112)
    for row_idx, row in enumerate(game_board):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, block_color, (col_idx * CELL_SIZE, row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_shape(shape, pos_x, pos_y, color):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                x = pos_x + col_idx * CELL_SIZE
                y = pos_y + row_idx * CELL_SIZE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

def clear_full_lines_and_columns():
    global game_board, score
    lines_cleared = 0

    for row_idx in range(GRID_SIZE):
        if all(game_board[row_idx]):
            game_board[row_idx] = [0] * GRID_SIZE
            lines_cleared += 1

    for col_idx in range(GRID_SIZE):
        if all(game_board[row][col_idx] for row in range(GRID_SIZE)):
            for row in range(GRID_SIZE):
                game_board[row][col_idx] = 0
            lines_cleared += 1

    score += lines_cleared * 10

def can_place_shape(shape, grid_x, grid_y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board_x, board_y = grid_x + col_idx, grid_y + row_idx
                if board_x >= GRID_SIZE or board_y >= GRID_SIZE or game_board[board_y][board_x] == 1:
                    return False
    return True

def can_place_anywhere(shape):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if can_place_shape(shape, x, y):
                return True
    return False

menu.show_menu(screen)

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (shape, (shape_x, shape_y)) in enumerate(zip(current_shapes, shape_positions)):
                if not placed_shapes[i]:
                    shape_rect = pygame.Rect(shape_x, shape_y, len(shape[0]) * CELL_SIZE, len(shape) * CELL_SIZE)
                    if shape_rect.collidepoint(mouse_x, mouse_y):
                        dragging = True
                        selected_shape = i

        if event.type == pygame.MOUSEMOTION and dragging:
            if selected_shape is not None:
                shape_w = len(current_shapes[selected_shape][0]) * CELL_SIZE
                shape_h = len(current_shapes[selected_shape]) * CELL_SIZE
                shape_positions[selected_shape] = (max(0, min(WIDTH - shape_w, mouse_x - shape_w // 2)),
                                                   max(0, min(HEIGHT - BOTTOM_PANEL_HEIGHT - shape_h, mouse_y - shape_h // 2)))

        if event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            if selected_shape is not None and not placed_shapes[selected_shape]:
                shape_x, shape_y = shape_positions[selected_shape]
                grid_x, grid_y = round(shape_x / CELL_SIZE), round(shape_y / CELL_SIZE)

                if can_place_shape(current_shapes[selected_shape], grid_x, grid_y):
                    for row_idx, row in enumerate(current_shapes[selected_shape]):
                        for col_idx, cell in enumerate(row):
                            if cell:
                                game_board[grid_y + row_idx][grid_x + col_idx] = 1

                    placed_shapes[selected_shape] = True
                    clear_full_lines_and_columns()

                    if all(placed_shapes):
                        current_shapes = generate_shapes()
                        shape_positions = [(100, 620), (250, 620), (400, 620)]
                        placed_shapes = [False, False, False]

                    if not any(can_place_anywhere(shape) for shape in current_shapes):
                        if game_over.show_game_over_screen(screen, score):
                            # Перезапуск игры
                            game_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                            current_shapes = generate_shapes()
                            shape_positions = [(100, 620), (250, 620), (400, 620)]
                            placed_shapes = [False, False, False]
                            score = 0
                        else:
                            running = False

    screen.fill((0, 0, 0))
    pygame.display.set_caption(f"Block Master - Очки: {score}")

    draw_grid()
    draw_board()

    for i, (shape, (x, y)) in enumerate(zip(current_shapes, shape_positions)):
        if not placed_shapes[i]:
            draw_shape(shape, x, y, (75, 0, 130))

    pygame.display.flip()

pygame.quit()
