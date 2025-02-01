import random

SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1]],

    [[1],
     [1],
     [1]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[0, 1, 1],
     [1, 1, 0]]
]


def get_random_shape():
    return random.choice(SHAPES)
