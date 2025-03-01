import pygame
import random
import menu
import game_over
import settings
from shapes import get_random_shape, get_helpful_shape

pygame.init()

WIDTH, HEIGHT = 600, 700
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
BOTTOM_PANEL_HEIGHT = 100
GRID_COLOR = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Master")

pygame.mixer.music.load("assets/music.mp3")
if settings.config["music"]:
    pygame.mixer.music.play(-1)

clear_sound = pygame.mixer.Sound("assets/sounds/cloth1.mp3")
clear_sound.set_volume(settings.config["volume"])

game_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
placed_blocks = {}
score = 0


def generate_shapes():
    return [get_random_shape() if random.random() > 0.2 else get_helpful_shape(game_board) for _ in range(3)]


def draw_textured_block(surface, x, y, size, color):
    pygame.draw.rect(surface, color, (x, y, size, size))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, size, size), 2)
    pygame.draw.rect(surface, (0, 0, 0), (x + 3, y + 3, size - 6, size - 6), 1)


current_shapes = generate_shapes()
shape_positions = [(100, 620), (250, 620), (400, 620)]
placed_shapes = [False, False, False]
shape_colors = [settings.generate_random_color() for _ in range(3)]
selected_shape = None
dragging = False
original_position = None


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT - BOTTOM_PANEL_HEIGHT))
    for y in range(0, HEIGHT - BOTTOM_PANEL_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_board():
    for (x, y), color in placed_blocks.items():
        block_color = color
        draw_textured_block(screen, x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, block_color)


def draw_shape(shape, pos_x, pos_y, color):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                x = pos_x + col_idx * CELL_SIZE
                y = pos_y + row_idx * CELL_SIZE
                draw_textured_block(screen, x, y, CELL_SIZE, color)


def can_place_shape(shape, grid_x, grid_y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                board_x, board_y = grid_x + col_idx, grid_y + row_idx
                if board_x >= GRID_SIZE or board_y >= GRID_SIZE or game_board[board_y][board_x] == 1:
                    return False
    return True


def clear_full_lines_and_columns():
    global game_board, placed_blocks, score
    full_rows = [row_idx for row_idx in range(GRID_SIZE) if all(game_board[row_idx])]
    full_cols = [col_idx for col_idx in range(GRID_SIZE) if all(game_board[row][col_idx] for row in range(GRID_SIZE))]

    if full_rows or full_cols:
        if settings.config["effects"]:
            clear_sound.play()

    for row_idx in full_rows:
        game_board[row_idx] = [0] * GRID_SIZE
        for x in range(GRID_SIZE):
            placed_blocks.pop((x, row_idx), None)
    for col_idx in full_cols:
        for row in range(GRID_SIZE):
            game_board[row][col_idx] = 0
            placed_blocks.pop((col_idx, row), None)
    score += (len(full_rows) + len(full_cols)) * 10


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
                        original_position = (shape_x, shape_y)
        if event.type == pygame.MOUSEMOTION and dragging:
            if selected_shape is not None:
                shape_w = len(current_shapes[selected_shape][0]) * CELL_SIZE
                shape_h = len(current_shapes[selected_shape]) * CELL_SIZE
                shape_positions[selected_shape] = (max(0, min(WIDTH - shape_w, mouse_x - shape_w // 2)),
                                                   max(0, min(HEIGHT - BOTTOM_PANEL_HEIGHT - shape_h,
                                                              mouse_y - shape_h // 2)))
        if event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            if selected_shape is not None and not placed_shapes[selected_shape]:
                shape_x, shape_y = shape_positions[selected_shape]
                grid_x, grid_y = round(shape_x / CELL_SIZE), round(shape_y / CELL_SIZE)
                if can_place_shape(current_shapes[selected_shape], grid_x, grid_y):
                    shape_color = shape_colors[selected_shape]
                    for row_idx, row in enumerate(current_shapes[selected_shape]):
                        for col_idx, cell in enumerate(row):
                            if cell:
                                game_board[grid_y + row_idx][grid_x + col_idx] = 1
                                placed_blocks[(grid_x + col_idx, grid_y + row_idx)] = shape_color
                    placed_shapes[selected_shape] = True
                    clear_full_lines_and_columns()
                    if all(placed_shapes):
                        current_shapes = generate_shapes()
                        shape_positions = [(100, 620), (250, 620), (400, 620)]
                        placed_shapes = [False, False, False]
                        shape_colors = [settings.generate_random_color() for _ in range(3)]
                    if not any(can_place_anywhere(shape) for shape in current_shapes):
                        if game_over.show_game_over_screen(screen, score):
                            game_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                            placed_blocks.clear()
                            current_shapes = generate_shapes()
                            shape_positions = [(100, 620), (250, 620), (400, 620)]
                            placed_shapes = [False, False, False]
                            shape_colors = [settings.generate_random_color() for _ in range(3)]
                            score = 0
                        else:
                            running = False
                else:
                    shape_positions[selected_shape] = original_position
    screen.fill((0, 0, 0))
    pygame.display.set_caption(f"Block Master - Очки: {score}")
    draw_grid()
    draw_board()
    for i, (shape, (x, y)) in enumerate(zip(current_shapes, shape_positions)):
        if not placed_shapes[i]:
            draw_shape(shape, x, y, shape_colors[i])
    pygame.display.flip()

pygame.quit()