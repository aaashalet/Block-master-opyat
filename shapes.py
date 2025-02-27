import random

SHAPES = [
    [[1]],

    [[1, 1]],
    [[1], [1]],

    [[1, 1, 1]],
    [[1], [1], [1]],
    [[1, 1], [0, 1]],
    [[0, 1], [1, 1]],
    [[1, 1], [1, 0]],

    [[1, 1], [1, 1]],
    [[1, 1, 1, 1]],
    [[1], [1], [1], [1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[0, 0, 1], [1, 1, 1]],

    [[1, 1, 1, 1, 1]],
    [[1], [1], [1], [1], [1]],
    [[1, 1, 1], [1, 0, 1]],
    [[1, 1, 1], [0, 1, 0], [0, 1, 0]],
    [[1, 1, 1, 1], [0, 1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [1, 0, 0], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
]


def get_random_shape():
    return random.choice(SHAPES)


def can_fit(shape, board):
    for r in range(len(board) - len(shape) + 1):
        for c in range(len(board[0]) - len(shape[0]) + 1):
            if all(
                    shape[i][j] == 0 or board[r + i][c + j] == 0
                    for i in range(len(shape))
                    for j in range(len(shape[0]))
            ):
                return True
    return False


def get_helpful_shape(game_board):
    possible_shapes = [shape for shape in SHAPES if can_fit(shape, game_board)]
    return random.choice(possible_shapes) if possible_shapes else get_random_shape()


def get_three_shapes(game_board, chance=50):
    while True:
        shapes = [get_random_shape() for _ in range(3)]

        if random.randint(1, 100) <= chance:
            for i in range(3):
                if not can_fit(shapes[i], game_board):
                    shapes[i] = get_helpful_shape(game_board)
                    break

        if any(can_fit(shape, game_board) for shape in shapes):
            return shapes


def is_game_over(game_board, remaining_shapes):
    return not any(can_fit(shape, game_board) for shape in remaining_shapes)


def update_game_state(game_board, shapes):
    if is_game_over(game_board, shapes):
        print("Игра окончена!")


def get_scaled_shape(shape, scale):
    return [[cell * scale for cell in row] for row in shape]


def draw_shape(shape, x, y, surface, size):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, (255, 255, 255),
                                 pygame.Rect(x + col_idx * size, y + row_idx * size, size, size))
