import pygame
import os
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, GREEN
from checkers.game import Game
from algorithm.alpha_beta_pruning import alpha_beta_pruning
from algorithm.minimax import minimax
from algorithm.iddfs import iddfs
from algorithm.negamax import negamax
from algorithm.mcts import mcts_move
from player_stats import PlayerStats

# Initialize Pygame
pygame.init()
pygame.font.init()

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Initialize player statistics
player_stats = PlayerStats()

# Color definitions
BG_COLOR = (240, 248, 255)  # Light Alice Blue
TITLE_COLOR = (255, 255, 255)  # White
BUTTON_NORMAL = (135, 206, 235)  # Sky Blue
BUTTON_HOVER = (70, 130, 180)  # Steel Blue
TEXT_NORMAL = (255, 255, 255)  # White
TEXT_HOVER = (245, 245, 220)  # Beige
TEXT_BLACK = (0, 0, 0)  # Black

# Fonts
FONT = pygame.font.Font(None, 36)
HOVER_FONT = pygame.font.Font(None, 40)
TITLE_FONT = pygame.font.Font(None, 48)

try:
    BACKGROUND_IMAGE = pygame.image.load("background.jpg")
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
except:
    BACKGROUND_IMAGE = None  # Fallback to solid color if image fails

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def reset_stats():
    """Reset player statistics"""
    if os.path.exists("player_stats.json"):
        os.remove("player_stats.json")
    # Create a new stats file with default values
    stats = PlayerStats()
    stats.save_stats()
    
    # Show confirmation
    if BACKGROUND_IMAGE:
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        WIN.fill(BG_COLOR)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 150))  # Gray with alpha
    WIN.blit(overlay, (0, 0))
    
    reset_text = TITLE_FONT.render("Statistics have been reset!", True, TITLE_COLOR)
    reset_rect = reset_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(reset_text, reset_rect)
    pygame.display.update()
    pygame.time.delay(1500)  # Show message for 1.5 seconds

def draw_menu(selected_option=None):
    """Draws the menu screen for AI selection with interactive buttons."""
    if BACKGROUND_IMAGE:
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        WIN.fill(BG_COLOR)
    
    # Semi-transparent overlay for better text readability
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 150))  # Gray with alpha
    WIN.blit(overlay, (0, 0))
    
    # Get the recommended level
    recommended = player_stats.get_recommended_level()
    
    # Title
    title_text = TITLE_FONT.render("Checkers Game", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    WIN.blit(title_text, title_rect)
    
    subtitle_text = FONT.render("Select an Algorithm", True, TITLE_COLOR)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    WIN.blit(subtitle_text, subtitle_rect)

    # Button properties
    button_width = 420
    button_height = 50
    button_spacing = 20
    start_y = HEIGHT // 4
    
    # Button options
    options = [
        ("1. Iterative Deepening DFS (Professional)", iddfs),
        ("2. MonteCarlo (Challenging PLACEHOLDER)", mcts_move),
        ("3. Alpha-Beta Pruning (Hard)", alpha_beta_pruning),
        ("4. Minimax (Medium)", minimax),
        ("5. ExpectiMax (Easy PLACEHOLDER)", None),
        ("6. Negamax (Beginner)", negamax),
        ("7. View Statistics", None)
    ]
    
    button_rects = []
    mouse_pos = pygame.mouse.get_pos()
    
    for i, (text, _) in enumerate(options):
        button_x = (WIDTH - button_width) // 2
        button_y = start_y + (button_height + button_spacing) * i
        
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_rects.append(button_rect)
        
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Draw button with shadow effect
        shadow_rect = pygame.Rect(button_x + 3, button_y + 3, button_width, button_height)
        pygame.draw.rect(WIN, (20, 20, 20, 50), shadow_rect, border_radius=10)
        
        if is_hovered or selected_option == i:
            pygame.draw.rect(WIN, BUTTON_HOVER, button_rect, border_radius=10)
            text_surface = HOVER_FONT.render(text, True, TEXT_HOVER)
        else:
            pygame.draw.rect(WIN, BUTTON_NORMAL, button_rect, border_radius=10)
            text_surface = FONT.render(text, True, TEXT_NORMAL)
            
        text_rect = text_surface.get_rect(center=button_rect.center)
        WIN.blit(text_surface, text_rect)
    
    # Add recommendation text at the bottom
    rec_text = FONT.render(f"Recommended Level: {recommended}", True, TITLE_COLOR)
    rec_rect = rec_text.get_rect(center=(WIDTH // 2, HEIGHT - 630))
    WIN.blit(rec_text, rec_rect)
    
    pygame.display.update()
    return button_rects, options  # Return options along with button_rects

def show_stats_screen():
    """Display statistics screen with enhanced visuals"""
    if BACKGROUND_IMAGE:
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        WIN.fill(BG_COLOR)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 180))
    WIN.blit(overlay, (0, 0))
    
    # Get the player stats
    player_name = player_stats.stats["player_name"]
    total_games = player_stats.stats["total_games"]
    recommended = player_stats.get_recommended_level()

    # Create text renderings
    title_text = TITLE_FONT.render("Player Statistics", True, TITLE_COLOR)
    name_text = FONT.render(f"Player: {player_name}", True, TITLE_COLOR)
    games_text = FONT.render(f"Total Games: {total_games}", True, TITLE_COLOR)
    
    # Level stats
    level_stats = []
    for i in range(1, 7):
        level_name = player_stats.stats["levels"][str(i)]["name"]
        level_stats.append(get_level_stats_text(i, level_name))
    
    rec_text = FONT.render(f"Recommended Level: {recommended}", True, TITLE_COLOR)
    back_text = FONT.render("Press any key to return to menu", True, TITLE_COLOR)
    
    # Panel for stats
    panel_width = 480
    panel_height = 420
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2
    
    # Draw panel with shadow
    shadow_rect = pygame.Rect(panel_x + 5, panel_y + 5, panel_width, panel_height)
    pygame.draw.rect(WIN, (20, 20, 20, 100), shadow_rect, border_radius=15)
    
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(WIN, (70, 130, 180, 200), panel_rect, border_radius=15)
    
    # Position and render the text
    title_rect = title_text.get_rect(center=(WIDTH // 2, panel_y + 30))
    WIN.blit(title_text, title_rect)
    
    text_x = panel_x + 30
    WIN.blit(name_text, (text_x, panel_y + 70))
    WIN.blit(games_text, (text_x, panel_y + 110))
    
    for i, stats_text in enumerate(level_stats):
        WIN.blit(stats_text, (text_x, panel_y + 150 + i * 35))
    
    rec_rect = rec_text.get_rect(center=(WIDTH // 2, panel_y + 370))
    WIN.blit(rec_text, rec_rect)
    
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    WIN.blit(back_text, back_rect)
    
    pygame.display.update()
    
    # Wait for key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def get_level_stats_text(level_num, level_name):
    """Helper function to create formatted level stats text"""
    level = str(level_num)
    wins = player_stats.stats["levels"][level]["wins"]
    losses = player_stats.stats["levels"][level]["losses"]
    total = wins + losses
    
    if total > 0:
        win_rate = (wins / total) * 100
        return FONT.render(f"{level}. {level_name}: {wins}W/{losses}L ({win_rate:.1f}%)", True, TITLE_COLOR)
    else:
        return FONT.render(f"{level}. {level_name}: No games played", True, TITLE_COLOR)

def select_algorithm():
    """Allows the user to select an AI algorithm before starting the game."""
    selected_option = None
    button_rects = None
    
    while selected_option is None:
        button_rects, options = draw_menu(selected_option)  # Get options from draw_menu
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 6:  # Stats button
                            show_stats_screen()
                            break
                        elif options[i][1] is None:  # Skip placeholders
                            break
                        else:
                            selected_option = i
                            break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_option = 0
                elif event.key == pygame.K_2:
                    selected_option = 1
                elif event.key == pygame.K_3:
                    selected_option = 2
                elif event.key == pygame.K_4:
                    selected_option = 3
                elif event.key == pygame.K_5:
                    selected_option = 4
                elif event.key == pygame.K_6:
                    selected_option = 5
                elif event.key == pygame.K_7:
                    show_stats_screen()
                elif event.key == pygame.K_r:
                    reset_stats()

    algorithms = [iddfs, mcts_move, alpha_beta_pruning, minimax, iddfs, negamax]
    return algorithms[selected_option], selected_option + 1  # Return algorithm and level

def show_end_message(winner, level):
    """Display game over screen with winner information and update stats."""
    # Update player statistics based on the winner
    player_won = winner == RED
    player_stats.update_stats(level, player_won)
    
    if BACKGROUND_IMAGE:
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        WIN.fill(BG_COLOR)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 180))
    WIN.blit(overlay, (0, 0))
    
    if winner == RED:
        winner_text = "You Won!"
        color = (255, 69, 0)  # Orange Red for player victory
    elif winner == WHITE:
        winner_text = "AI Won!"
        color = (70, 130, 180)  # Steel Blue for AI victory
    else:
        winner_text = "It's a Draw!"
        color = TITLE_COLOR
    
    # Draw panel for message
    panel_width = 400
    panel_height = 200
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2
    
    # Shadow effect
    shadow_rect = pygame.Rect(panel_x + 5, panel_y + 5, panel_width, panel_height)
    pygame.draw.rect(WIN, (20, 20, 20, 100), shadow_rect, border_radius=15)
    
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(WIN, (40, 40, 40, 220), panel_rect, border_radius=15)
    
    winner_surface = TITLE_FONT.render(winner_text, True, color)
    winner_rect = winner_surface.get_rect(center=(WIDTH // 2, panel_y + 70))
    WIN.blit(winner_surface, winner_rect)
    
    instruction_surface = FONT.render("Press any key to close", True, TITLE_COLOR)
    instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, panel_y + 130))
    WIN.blit(instruction_surface, instruction_rect)
    
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    ai_algorithm, level = select_algorithm()  # Ask the user for AI choice
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            if ai_algorithm == mcts_move:  # Special case for MCTS
                move = ai_algorithm(game.get_board(), WHITE)
                if move:
                    piece, destination = move
                    game.select(piece.row, piece.col)
                    row, col = destination
                    game._move(row, col)
            else:
                value, new_board = ai_algorithm(game.get_board(), 3, WHITE, game)
                game.ai_move(new_board)

        if game.winner() is not None:
            print(f"Winner: {game.winner()}")
            show_end_message(game.winner(), level)
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

if __name__ == "__main__":
    main()