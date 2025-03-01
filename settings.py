import random
import pygame

config = {
    "volume": 1.0,
    "effects": True,
    "music": True
}

def apply_settings():
    if config["music"]:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

def generate_random_color():
    return random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)])
