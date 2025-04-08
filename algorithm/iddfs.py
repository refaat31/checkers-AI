from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def iddfs(position, max_depth, max_player, game):
    best_move = None
    best_value = float('-inf') if max_player else float('inf')  # Track best evaluation

    for depth in range(1, max_depth + 1):  # Iteratively increase depth
        eval, move = depth_limited_search(position, depth, max_player, game)
        if move:  # If a move is found
            best_value = eval  # Update best evaluation
            best_move = move   # Update best move found so far

    if best_move is None:  # No moves found at any depth
        return position.evaluate(), position  # Return current evaluation and position
    
    return best_value, best_move  # Return tuple of best evaluation and move

def depth_limited_search(position, depth, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(position, WHITE, game)
        if not moves:  # No moves available
            return position.evaluate(), position
        for move in moves:
            evaluation, _ = depth_limited_search(move, depth - 1, False, game)
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(position, RED, game)
        if not moves:  # No moves available
            return position.evaluate(), position
        for move in moves:
            evaluation, _ = depth_limited_search(move, depth - 1, True, game)
            if evaluation < minEval:
                minEval = evaluation
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
            draw_moves(game, board)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves

def draw_moves(game, board):
    pygame.draw.circle(game.win, (0, 255, 0), (280, 280), 50, 5)
    pygame.display.update()