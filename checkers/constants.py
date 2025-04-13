# constants.py
import pygame

WIDTH, HEIGHT = 800, 800  # Increased from 560x560
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS  # Now 100 (800 // 8)

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (SQUARE_SIZE // 2, SQUARE_SIZE // 4))