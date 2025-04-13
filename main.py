import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, GREEN
from checkers.game import Game
from algorithm.alpha_beta_pruning import alpha_beta_pruning
from algorithm.minimax import minimax
from algorithm.iddfs import iddfs
from algorithm.mcts import mcts_move

# Initialize Pygame
pygame.init()
pygame.font.init()


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')



FONT = pygame.font.Font(None, 36)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def draw_menu():
    """Draws the menu screen for AI selection."""
    WIN.fill(WHITE)

    title_text = FONT.render("Select an algorithm (e.g. 1 for Minimax)", True, BLACK)
    minimax_text = FONT.render("1. Minimax", True, BLACK)
    alpha_beta_text = FONT.render("2. Alpha-Beta Pruning", True, BLACK)
    iddfs_text = FONT.render("3. Iterative Deepening DFS", True, BLACK)
    mcts_text = FONT.render("4. MCTS", True, BLACK)

    WIN.blit(title_text, (WIDTH // 5 , HEIGHT // 10 ))
    WIN.blit(minimax_text, (WIDTH // 5 , HEIGHT // 10 * 3))
    WIN.blit(alpha_beta_text, (WIDTH // 5 , HEIGHT // 10 * 4))
    WIN.blit(iddfs_text, (WIDTH // 5 , HEIGHT // 10 * 5))
    WIN.blit(mcts_text, (WIDTH // 5 , HEIGHT // 10 * 6))

    pygame.display.update()

def select_algorithm():
    """Allows the user to select an AI algorithm before starting the game."""
    draw_menu()
    selected_algorithm = None

    while selected_algorithm is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return minimax
                elif event.key == pygame.K_2:
                    return alpha_beta_pruning
                elif event.key == pygame.K_3:
                    return iddfs
                elif event.key == pygame.K_4:
                    return mcts_move
                
def show_end_message():
    WIN.fill(WHITE)
    end_text = FONT.render("Game Ended. Press any key to close.", True, GREEN)
    WIN.blit(end_text, (WIDTH // 2 - 180, HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    ai_algorithm = select_algorithm()  # Ask the user for AI choice
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            if ai_algorithm == mcts_move:  # Special case for MCTS
                print(game.get_board())
                move = ai_algorithm(game.get_board(), WHITE)
                piece, destination = move
                game.select(piece.row, piece.col)
                row, col = destination
                game._move(row, col)
            else:
                value, new_board = ai_algorithm(game.get_board(), 3, WHITE, game)
                game.ai_move(new_board)

        if game.winner() is not None:
            print(f"Winner: {game.winner()}")
            show_end_message()
            #pygame.time.delay(2000)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == RED:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()
