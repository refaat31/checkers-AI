from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def iddfs(position, max_depth, max_player, game):
    best_eval = float('-inf') if max_player else float('inf')
    best_move = None
 
    for depth in range(1, max_depth + 1): # Iteratively increase depth
        eval_value, move = depth_limited_search(position, depth, max_player, game)
        if max_player and eval_value > best_eval:
            best_eval = eval_value
            best_move = move
        elif not max_player and eval_value < best_eval:
            best_eval = eval_value # Update best move found so far    
            best_move = move # Return the best move found in the deepest search
    
    if best_move is None:
        return position.evaluate(), position
        
    return best_eval, best_move

def depth_limited_search(position, depth, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation, _ = depth_limited_search(move, depth - 1, False, game)
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
        
        if best_move is None:
            return position.evaluate(), position
            
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation, _ = depth_limited_search(move, depth - 1, True, game)
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
                
        if best_move is None:
            return position.evaluate(), position
            
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

def draw_moves(game, board):
    if game:
        pygame.draw.circle(game.win, (0, 255, 0), (280, 280), 50, 5)
        pygame.display.update()