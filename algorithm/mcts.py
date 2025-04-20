
import math
import random
from copy import deepcopy
from checkers.constants import RED, WHITE

class MCTSNode:
    def __init__(self, board, turn, parent=None, move=None):
        self.board = board
        self.turn = turn
        self.parent = parent
        self.children = []
        self.move = move  # (piece, destination)
        self.visits = 0
        self.wins = 0

        all_moves = board.get_all_valid_moves(turn)
        self.untried_moves = [(piece, move) for piece, moves in all_moves.items() for move in moves]

    def ucb1(self, total_simulations, exploration=1.41):
        if self.visits == 0:
            return float('inf')
        win_rate = self.wins / self.visits
        return win_rate + exploration * math.sqrt(math.log(total_simulations) / self.visits)

    def best_child(self):
        total_simulations = sum(child.visits for child in self.children)
        return max(self.children, key=lambda child: child.ucb1(total_simulations))

    def expand(self):
        move = self.untried_moves.pop()
        board_copy = deepcopy(self.board)
        piece, destination = move

        row, col = piece.row, piece.col
        dest_row, dest_col = destination

        piece_copy = board_copy.get_piece(row, col)
        board_copy.move(piece_copy, dest_row, dest_col)

        next_turn = RED if self.turn == WHITE else WHITE
        child_node = MCTSNode(board_copy, next_turn, parent=self, move=move)
        self.children.append(child_node)

        print(f"[Expand] Expanded node: {piece} to {destination}, next turn: {'WHITE' if next_turn == WHITE else 'RED'}")
        return child_node

    def is_terminal_node(self):
        return self.board.winner() is not None

    def simulate(self, max_depth=1000):
        sim_board = deepcopy(self.board)
        turn = self.turn
        depth = 0

        while not sim_board.winner() and depth < max_depth:
            all_moves = sim_board.get_all_valid_moves(turn)
            if not all_moves:
                print(f"[Simulate] No moves available for {'WHITE' if turn == WHITE else 'RED'} at depth {depth}")
                break

            # piece = random.choice(list(all_moves.keys()))
            # move = random.choice(list(all_moves[piece].keys()))

            # Get all available pieces and their possible moves
            pieces = list(all_moves.keys())
            
            # Step 1: Prioritize captures if available
            capture_pieces = []
            for piece in pieces:
                for move in all_moves[piece]:
                    dest_row, dest_col = move
                    # Check if this is a capture move (jumps more than one square)
                    if abs(piece.row - dest_row) > 1:
                        capture_pieces.append((piece, move))
            
            # Step 2: Prioritize king promotions if available and no captures
            promotion_pieces = []
            if not capture_pieces:
                for piece in pieces:
                    if not piece.king:  # Only consider non-king pieces
                        for move in all_moves[piece]:
                            dest_row, dest_col = move
                            # Check if this move would result in a king promotion
                            if (turn == WHITE and dest_row == 0) or (turn == RED and dest_row == 7):
                                promotion_pieces.append((piece, move))
            
            # Step 3: Make a weighted random choice based on our priorities
            if capture_pieces:
                # Always choose a capture when available
                piece, move = random.choice(capture_pieces)
            elif promotion_pieces:
                # Choose a king promotion when available and no captures
                piece, move = random.choice(promotion_pieces)
            else:
                # No captures or promotions, use a simple heuristic
                weighted_moves = []
                for piece in pieces:
                    for move in all_moves[piece]:
                        dest_row, dest_col = move
                        weight = 1.0  # Base weight
                        
                        # Kings are valuable - prefer keeping them safe in center
                        if piece.king:
                            # Center positions get higher weights
                            center_weight = 4 - abs(3.5 - dest_col) - abs(3.5 - dest_row)
                            weight *= (1.0 + 0.2 * center_weight)
                        else:
                            # Non-kings: prefer advancing toward opponent's side
                            if turn == WHITE:
                                # WHITE pieces want to advance toward row 0
                                progress = piece.row - dest_row
                            else:
                                # RED pieces want to advance toward row 7
                                progress = dest_row - piece.row
                            
                            # Give more weight to forward moves
                            weight *= (1.0 + 0.3 * progress)
                        
                        weighted_moves.append((piece, move, weight))
                
                # Choose move based on weights
                total_weight = sum(w for _, _, w in weighted_moves)
                r = random.uniform(0, total_weight)
                cumulative_weight = 0
                for piece, move, weight in weighted_moves:
                    cumulative_weight += weight
                    if cumulative_weight >= r:
                        break

            # Execute the selected move
            row, col = piece.row, piece.col
            dest_row, dest_col = move

            piece_copy = sim_board.get_piece(row, col)
            sim_board.move(piece_copy, dest_row, dest_col)

            turn = RED if turn == WHITE else WHITE
            depth += 1

        winner = sim_board.winner()
        print(f"[Simulate] Simulation ended at depth {depth}. Winner: {winner}")
        return 1 if winner == self.turn else 0

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)

def mcts_move(board, turn, iterations=500):
    if board.winner():
        print("[MCTS] Early exit: board already has a winner")
        return None
    board_copy = deepcopy(board)
    root = MCTSNode(board_copy, turn)

    for i in range(iterations):
        if i % 50 == 0:
            print(f"[MCTS] Iteration {i}")
        node = root
        # Selection
        while node.untried_moves == [] and node.children:
            node = node.best_child()

        # Expansion
        if node.untried_moves:
            node = node.expand()

        # Simulation
        result = node.simulate()

        # Backpropagation
        node.backpropagate(result)

    if not root.children:
        print("[MCTS] No children were expanded — returning random valid move")
        all_moves = board.get_all_valid_moves(turn)
        if not all_moves:
            return None
        piece = random.choice(list(all_moves.keys()))
        move = random.choice(list(all_moves[piece].keys()))
        return piece, move

    best = max(root.children, key=lambda n: n.visits)
    return best.move
