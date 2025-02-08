import pygame
import menu 
from shapes import get_random_shape

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Master")

GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
GRID_COLOR = (50, 50, 50)

BOTTOM_PANEL_HEIGHT = 100

game_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

current_shapes = [get_random_shape() for _ in range(3)]
selected_shape = None
shape_positions = [(100, 620), (250, 620), (400, 620)]
dragging = False
placed_shapes = [False, False, False]

score = 0


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT - BOTTOM_PANEL_HEIGHT))
    for y in range(0, HEIGHT - BOTTOM_PANEL_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_shape(shape, pos_x, pos_y, color):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                x = pos_x + col_idx * CELL_SIZE
                y = pos_y + row_idx * CELL_SIZE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))


def draw_board():
    block_color = (25, 25, 112)
    for row_idx, row in enumerate(game_board):
        for col_idx, cell in enumerate(row):
            if cell:
                x = col_idx * CELL_SIZE
                y = row_idx * CELL_SIZE
                pygame.draw.rect(screen, block_color, (x, y, CELL_SIZE, CELL_SIZE))


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
                board_x = grid_x + col_idx
                board_y = grid_y + row_idx
                if board_x >= GRID_SIZE or board_y >= GRID_SIZE or board_x < 0 or board_y < 0 or game_board[board_y][
                    board_x] == 1:
                    return False
    return True


def can_place_anywhere(shape):
    for grid_y in range(GRID_SIZE):
        for grid_x in range(GRID_SIZE):
            if can_place_shape(shape, grid_x, grid_y):
                return True
    return False


menu.show_menu(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, (shape, (shape_x, shape_y)) in enumerate(zip(current_shapes, shape_positions)):
                if not placed_shapes[i]:
                    shape_rect = pygame.Rect(shape_x, shape_y, len(shape[0]) * CELL_SIZE, len(shape) * CELL_SIZE)
                    if shape_rect.collidepoint(mouse_x, mouse_y):
                        dragging = True
                        selected_shape = i

        if event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            shape_positions[selected_shape] = (mouse_x - (len(current_shapes[selected_shape][0]) * CELL_SIZE) // 2,
                                               mouse_y - (len(current_shapes[selected_shape]) * CELL_SIZE) // 2)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            if selected_shape is not None and not placed_shapes[selected_shape]:
                shape_x, shape_y = shape_positions[selected_shape]
                grid_x = round(shape_x / CELL_SIZE)
                grid_y = round(shape_y / CELL_SIZE)

                if can_place_shape(current_shapes[selected_shape], grid_x, grid_y):
                    for row_idx, row in enumerate(current_shapes[selected_shape]):
                        for col_idx, cell in enumerate(row):
                            if cell:
                                game_board[grid_y + row_idx][grid_x + col_idx] = 1

                    placed_shapes[selected_shape] = True
                    selected_shape = None 

                    clear_full_lines_and_columns()

                    if all(placed_shapes):
                        current_shapes = [get_random_shape() for _ in range(3)]
                        shape_positions = [(100, 620), (250, 620), (400, 620)]
                        placed_shapes = [False, False, False]

                    if not any(can_place_anywhere(shape) for shape in current_shapes):
                        print("Игра окончена!")
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
