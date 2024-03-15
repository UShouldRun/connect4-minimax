import pygame
from screeninfo import get_monitors

pygame.init()

monitor1 = get_monitors()[0]
STARTING_SIZE_PERCENTAGE = 0.75
WIDTH, HEIGHT = monitor1.width * STARTING_SIZE_PERCENTAGE, monitor1.height * STARTING_SIZE_PERCENTAGE
TITLE = "Connect4"
MAIN_FONT = pygame.font.SysFont("Comic Sans", 72)

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'light_gray': (192, 192, 192),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
    'brown': (165, 42, 42),
    'pink': (255, 192, 203),
    'turquoise': (64, 224, 208),
    'gold': (255, 215, 0),
    'silver': (192, 192, 192),
    'navy_blue': (0, 0, 128),
    'olive_green': (128, 128, 0),
    'maroon': (128, 0, 0),
    'teal': (0, 128, 128),
    'sky_blue': (135, 206, 235),
    'indigo': (75, 0, 130),
    'violet': (238, 130, 238),
    'lavender': (230, 230, 250),
    'peach': (255, 218, 185),
    'coral': (255, 127, 80),
    'tan': (210, 180, 140),
    'khaki': (240, 230, 140),
    'orchid': (218, 112, 214),
    'salmon': (250, 128, 114),
    'beige': (245, 245, 220),
    'wheat': (245, 222, 179)
}

# Define constants for the board layout
SQUARE_SIZE = 100
LINES, COLUMNS = 6, 7
BOARD_WIDTH = COLUMNS * SQUARE_SIZE
BOARD_HEIGHT = LINES * SQUARE_SIZE
BOARD_TOP_LEFT_X = WIDTH//2 - BOARD_WIDTH//2
BOARD_TOP_LEFT_Y = HEIGHT - BOARD_HEIGHT

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
