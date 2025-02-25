from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    #Padding for the piece position in each square
    PADDING = 15
    #Outline for the piece in each square
    OUTLINE = 2
    # Each piece has position attribute (row,col), a color attribute (RED/WHITE), and a king mark
    def __init__(self, row, col, color):
        # row position for the piece
        self.row = row
        # column position for the piece
        self.col = col
        # color position for the piece
        self.color = color
        # If the piece is king or not
        self.king = False
        # Horizontal position will be stored
        self.x = 0
        # Vertical Position will be stored
        self.y = 0
        # Calculate the position of each piece
        self.calc_pos()

    def calc_pos(self):
        #Piece will be placed in the center of a square
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    
    def make_king(self):
        #If the piece is king, king attribute will be set
        self.king = True
    
    def draw(self, win):
        # radius of piece
        radius = SQUARE_SIZE//2 - self.PADDING
        # Creating an outline for a piece
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        #Inserting piece in its position
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        # Inserting a crown logo for the king
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        #Updating the (x,y) position of a piece
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        # returns the color of piece
        return str(self.color)
