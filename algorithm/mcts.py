
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

    def simulate(self, max_depth=100):
        sim_board = deepcopy(self.board)
        turn = self.turn
        depth = 0

        while not sim_board.winner() and depth < max_depth:
            all_moves = sim_board.get_all_valid_moves(turn)
            if not all_moves:
                print(f"[Simulate] No moves available for {'WHITE' if turn == WHITE else 'RED'} at depth {depth}")
                break

            piece = random.choice(list(all_moves.keys()))
            move = random.choice(list(all_moves[piece].keys()))

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

def mcts_move(board, turn, iterations=200):
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
