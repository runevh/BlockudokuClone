import time
from enum import Enum
import pygame


class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARKGRAY = (75, 75, 75)
    LIGHTGRAY = (150, 150, 150)


def renderText(screen, text, x, y, size=20, color=Color.BLACK, font_type="data/fonts/Roboto-Medium.ttf"):
    try:
        font = pygame.font.Font(font_type, size)
        text = font.render(str(text), True, color.value)
        screen.blit(text, (x, y))
    except Exception as e:
        print('Font Error')
        raise e


def get_current_millis():
    return round(time.time() * 1000)


def get_current_nanos():
    return time.time_ns()
