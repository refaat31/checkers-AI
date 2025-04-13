from copy import deepcopy
import pygame
from checkers.constants import RED, WHITE, SQUARE_SIZE, GREEN, WIDTH, HEIGHT  # Import from checkers.constants

def alpha_beta_pruning(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(position, WHITE, game)
        if not moves:  # No moves available
            return position.evaluate(), position
        for move in moves:
            evaluation = alpha_beta_pruning(move, depth - 1, False, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, maxEval)  # Update alpha
            if maxEval == evaluation:
                best_move = move
            if beta <= alpha:  # Prune the branch
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(position, RED, game)
        if not moves:  # No moves available
            return position.evaluate(), position
        for move in moves:
            evaluation = alpha_beta_pruning(move, depth - 1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, minEval)  # Update beta
            if minEval == evaluation:
                best_move = move
            if beta <= alpha:  # Prune the branch
                break
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves

def draw_moves(game, board):  # Fixed parameter to match get_all_moves call
    font = pygame.font.Font(None, SQUARE_SIZE // 2)  # Scale font size with SQUARE_SIZE
    text = font.render("Thinking", True, GREEN)  # Use GREEN from constants
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center for current window size
    game.win.blit(text, text_rect)
    pygame.display.update()