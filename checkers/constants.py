#List of Variables used
import pygame

WIDTH,HEIGHT = 560,560
ROWS,COLS = 8,8
SQUARE_SIZE=WIDTH//COLS #SQUARE SIZE=70

#rgb
RED=(255,0,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(128,128,128)
BLUE=(0,0,255)

# Crown image for king
CROWN=pygame.transform.scale(pygame.image.load('assets/crown.png'),(44,25))
