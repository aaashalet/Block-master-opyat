import random

SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1, 1],
     [1, 0, 1]]
]


def get_random_shape():
    return random.choice(SHAPES)


def get_smart_shape(game_board, chance=30):
    if random.randint(1, 100) <= chance:
        # Находим пустые места
        empty_cells = [(r, c) for r in range(len(game_board)) for c in range(len(game_board[0])) if
                       game_board[r][c] == 0]

        if empty_cells:
            r, c = random.choice(empty_cells)
            possible_shapes = [shape for shape in SHAPES if can_fit(shape, game_board, r, c)]

            if possible_shapes:
                return random.choice(possible_shapes)

    return get_random_shape()


def can_fit(shape, board, r, c):
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                if r + i >= len(board) or c + j >= len(board[0]) or board[r + i][c + j] == 1:
                    return False
    return True
