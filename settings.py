import random

settings = {
    "random_colors": True,
    "selected_color": (0, 255, 255),
    "glow_effect": False
}

def generate_random_color():
    return random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)])
