import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        # Setup board as an array
        self.board = []
        # Number of pieces on the board
        self.red_left = self.white_left = 12
        # Number of kings on the board
        self.red_kings = self.white_kings = 0
        # Create Board
        self.create_board()

    #Function to draw red and black patterns on a checker board
    def draw_squares(self, win):
        # Fill window with black color
        win.fill(BLACK)
        # Loop through each row
        for row in range(ROWS):
            # Loop through each column, starting from 0 or 1 based on whether the row is even or odd.
            # Loop will increment by 2, skipping alternate columns to create the checkered pattern.
            for col in range(row % 2, COLS, 2):
                # Draw red rectangle on the Pygame window
                # rect(window, color, (top left x-coordinate, top left y-coordinate, width, height))
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            # Creating an 2D array for the board
            self.board.append([])
            # inser pieces in each row
            for col in range(COLS):
                #Insert in alternating order
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        # White pieces will be inserted in row 0,1 and 2
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        # Red pieces will be inserted in row 5,6,7
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        # Rest of the empty squares wil be filled with 0
                        self.board[row].append(0)
                else:
                    # Rest of the empty squares wil be filled with 0
                    self.board[row].append(0)
        
    # Method for rendering the board and pieces on the window.
    def draw(self, win):
        # Call the draw_squares() method to draw the squares on the window
        # This colors the squares to create the RED-BLACK pattern.
        self.draw_squares(win)
        # Loop for rendring all the pieces on the squares
        for row in range(ROWS):
            for col in range(COLS):
                # Get the piece information located at each sqaure
                # piece = RED or BLACK or 0 ; three options
                piece = self.board[row][col]
                # Check if the piece 0 or the square is blank
                if piece != 0:
                    # If the square is not empty, 
                    # call the draw method in the Piece class to render it on the window
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        # If there is no Red piece left, White wins
        if self.red_left <= 0:
            return WHITE
        # If there is no white piece left, Red wins
        elif self.white_left <= 0:
            return RED
            
        #else return no winner
        return None 


    # Method to get the dictionary of valid moves
    def get_valid_moves(self, piece):
        # Initialize an empty dictionary to store valid moves
        moves = {}
        # Calculate the left column adjacent to the piece
        left = piece.col - 1
        # Calculate the right column adjacent to the piece
        right = piece.col + 1
        # Get the row of the piece
        row = piece.row

        if piece.color == RED or piece.king:
            # Traverse left diagonals upwards
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            # Traverse right diagonals upwards
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            # Traverse left diagonals downwards
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            # Traverse right diagonals downwards
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        # Initialize an empty dictionary to store valid moves
        moves = {}
        # Initialize an empty list to keep track of pieces to be skipped
        last = []
        for r in range(start, stop, step):
            # Check if the left column index is out of bounds
            if left < 0:
                break
            # Get the current square on the board
            current = self.board[r][left]
            # Check if the current square is empty
            if current == 0:
                # If there are skipped pieces but no piece to capture, stop traversal
                if skipped and not last:
                    break
                # If there are skipped pieces, add the move with the skipped pieces
                elif skipped:
                    moves[(r, left)] = last + skipped
                # If no pieces are skipped, add the move normally
                else:
                    moves[(r, left)] = last

                # If there is a piece to be captured
                if last:
                    # Determine the next row based on the direction of movement
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    # Recursively traverse left and right diagonals to find further valid moves
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            # If the current piece is the same color, stop traversal
            elif current.color == color:
                break
            # If the current piece is of the opposite color, mark it as the last piece to be captured
            else:
                last = [current]
            # Move to the next column on the left
            left -= 1
        # Return the dictionary of valid moves
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        # Initialize an empty dictionary to store valid moves
        moves = {}
        # Initialize an empty list to keep track of pieces to be skipped
        last = []
        for r in range(start, stop, step):
            
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
