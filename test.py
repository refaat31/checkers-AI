from checkers.game import Game
import pygame

pygame.init()
WIN = pygame.display.set_mode((800, 800))

game = Game(WIN)

# Get all valid moves for current player
valid_moves = game.get_all_valid_moves()
print("Turn:", "RED" if game.turn == (255, 0, 0) else "WHITE")
print("Valid Moves:")
for piece, moves in valid_moves.items():
    print(f"Piece at ({piece.row}, {piece.col}) → {list(moves.keys())}")