from copy import deepcopy
import pygame
from checkers.constants import RED, WHITE, SQUARE_SIZE, GREEN, WIDTH, HEIGHT

def negamax(position, depth, color, game):
    # Base case: depth 0 or game over
    if depth == 0 or position.winner() is not None:
        return evaluate_board(position, color), position

    maxEval = float('-inf')
    best_move = None
    moves = get_all_moves(position, color, game)
    
    if not moves:  # No moves available
        return evaluate_board(position, color), position

    for move in moves:
        evaluation = -negamax(move, depth-1, RED if color == WHITE else WHITE, game)[0]
        if evaluation > maxEval:
            maxEval = evaluation
            best_move = move

    return maxEval, best_move

def evaluate_board(board, color):
    # Initialize scores
    attack_score = 0
    king_safety_score = 0
    material_positional_score = 0
    endgame_score = 0

    # Count total pieces for endgame check
    total_pieces = len(board.get_all_pieces(RED)) + len(board.get_all_pieces(WHITE))
    is_endgame = total_pieces <= 6

    # Helper to check if a square is central
    def is_central(col):
        return col in [3, 4]

    # Helper to check if a square is on edge
    def is_edge(row, col):
        return row in [0, 7] or col in [0, 7]

    # Helper to check adjacent pieces
    def has_adjacent_ally(board, row, col, piece_color):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board.get_piece(r, c)
                if piece != 0 and piece.color == piece_color:
                    return True
        return False

    # Attack potential
    for c in [RED, WHITE]:
        multiplier = 1 if c == color else -1
        for piece in board.get_all_pieces(c):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                if skip:  # Capture move
                    attack_score += 5 * multiplier
                    # Check for multi-jump potential (simplified)
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    temp_board.move(temp_piece, move[0], move[1])
                    temp_board.remove(skip)
                    more_jumps = any(s for m, s in temp_board.get_valid_moves(temp_piece).items() if s)
                    if more_jumps:
                        attack_score += 2 * multiplier

        # Threatened pieces
        for piece in board.get_all_pieces(c):
            for opp_piece in board.get_all_pieces(RED if c == WHITE else WHITE):
                opp_moves = board.get_valid_moves(opp_piece)
                for move, skip in opp_moves.items():
                    if skip and any(s.row == piece.row and s.col == piece.col for s in skip):
                        attack_score -= 3 * multiplier

    # King safety
    for c in [RED, WHITE]:
        multiplier = 1 if c == color else -1
        for piece in board.get_all_pieces(c):
            if piece.king:
                if is_edge(piece.row, piece.col):
                    king_safety_score -= 2 * multiplier
                if is_central(piece.col):
                    king_safety_score += 3 * multiplier
                # Check if king is threatened
                for opp_piece in board.get_all_pieces(RED if c == WHITE else WHITE):
                    opp_moves = board.get_valid_moves(opp_piece)
                    for move, skip in opp_moves.items():
                        if skip and any(s.row == piece.row and s.col == piece.col for s in skip):
                            king_safety_score -= 5 * multiplier

    # Material and positional factors
    for c in [RED, WHITE]:
        multiplier = 1 if c == color else -1
        for piece in board.get_all_pieces(c):
            # Material
            if piece.king:
                material_positional_score += 15 * multiplier
            else:
                material_positional_score += 10 * multiplier
            # Advancement
            if c == WHITE:
                material_positional_score += (7 - piece.row) * multiplier
            else:  # RED
                material_positional_score += piece.row * multiplier
            # Center control
            if is_central(piece.col):
                material_positional_score += 2 * multiplier
            # Defensive structure
            if has_adjacent_ally(board, piece.row, piece.col, c):
                material_positional_score += 1 * multiplier

    # Endgame evaluation
    if is_endgame:
        # Material advantage
        white_pieces = len(board.get_all_pieces(WHITE))
        red_pieces = len(board.get_all_pieces(RED))
        material_diff = white_pieces - red_pieces
        endgame_score += 20 * material_diff * (1 if color == WHITE else -1)

        # King mobility
        for piece in board.get_all_pieces(color):
            if piece.king:
                endgame_score += 3 * len(board.get_valid_moves(piece)) * (1 if color == WHITE else -1)
        for piece in board.get_all_pieces(RED if color == WHITE else WHITE):
            if piece.king:
                endgame_score -= 3 * len(board.get_valid_moves(piece)) * (1 if color == WHITE else -1)

        # Trap bonus
        opp_color = RED if color == WHITE else WHITE
        opp_moves = get_all_moves(board, opp_color, game)
        if not opp_moves:
            endgame_score += 50 * (1 if color == WHITE else -1)

    # Combine scores
    total_score = attack_score + king_safety_score + material_positional_score
    if is_endgame:
        total_score += endgame_score

    return total_score

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
    font = pygame.font.Font(None, SQUARE_SIZE // 2)
    text = font.render("Thinking", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    game.win.blit(text, text_rect)
    pygame.display.update()