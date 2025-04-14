from copy import deepcopy
import pygame
from checkers.constants import RED, WHITE, SQUARE_SIZE, GREEN, WIDTH, HEIGHT
import random

def expectimax(position, depth, max_player, game):
    
    wrong_eval = 9999                   # Winning eval is 10,000
    # Setting this high but below 10,000 means even random behavior will not stop a winning move
    
    # Tuning bad ai behavior; choose any values, only relative sizes matter
    # higher random and bad values -> easy ai
    good_choice_frequency = 5       # normal behavior
    rand_choice_frequency = 1           # Choosing a random move as very good
    bad_choice_frequency = 1            # Flipping evaluations bad = good
    bad_behavior = 0
    
    bad_threshold = bad_choice_frequency/(good_choice_frequency+rand_choice_frequency+bad_choice_frequency)
    rand_threshold = 1 - (rand_choice_frequency/(good_choice_frequency+rand_choice_frequency+bad_choice_frequency))
    roll = random.random()
    
    
    if roll > rand_threshold:   #high roll = random choice
        moves = get_all_moves(position, WHITE, game)
        if not moves:  # No moves
            return position.evaluate(), position  # Return current state evaluation, no randomization
        choice = round(roll*(len(moves)-1))
        if max_player:
            return wrong_eval, moves[choice]
        else:
            return (-1 * wrong_eval), moves[choice]
        
    if roll<bad_threshold:      #low roll = bad choices
        bad_behavior = 1
    
    if depth == 0 or position.winner() != None:
        if bad_behavior:
            return (-1 * position.evaluate()), position
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(position, WHITE, game)
        if not moves:  # No moves available
            if bad_behavior:
                return (-1 * position.evaluate()), position
            return position.evaluate(), position  # Return current state evaluation
        for move in moves:
            evaluation = expectimax(move, depth-1, False, game)[0]
            if bad_behavior:
                evaluation = -1 * evaluation
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(position, RED, game)
        if not moves:  # No moves available
            return position.evaluate(), position  # Return current state evaluation
        for move in moves:
            evaluation = expectimax(move, depth-1, True, game)[0]
            if bad_behavior:
                evaluation = -1 * evaluation
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
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
            draw_moves(game)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves

def draw_moves(game):
    font = pygame.font.Font(None, SQUARE_SIZE // 2)  # Scale font size with SQUARE_SIZE (e.g., 50 for 100)
    text = font.render("Thinking", True, GREEN)  # Use GREEN from constants
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center at (400, 400) for 800x800
    game.win.blit(text, text_rect)
    pygame.display.update()