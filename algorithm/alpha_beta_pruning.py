from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255,255,255)

def alpha_beta_pruning(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
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
        for move in get_all_moves(position, RED, game):
            evaluation = alpha_beta_pruning(move, depth - 1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, minEval)  # Update beta
            if minEval == evaluation:
                best_move = move
            if beta <= alpha:  # Prune the branch
                break
        return minEval, best_move

def simulate_move(piece,move,board,game,skip):
    board.move(piece,move[0],move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board,color,game):
    moves=[]
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move,skip in valid_moves.items():
            draw_moves(game, board)
            temp_board = deepcopy(board)
            temp_piece=temp_board.get_piece(piece.row,piece.col)
            new_board= simulate_move(temp_piece,move,temp_board,game,skip)
            moves.append(new_board)
    return moves

def draw_moves(game, board):
    #board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (280, 280), 50, 5)
    pygame.display.update()
    #pygame.time.delay(100)