import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK, GREEN
from checkers.game import Game
from algorithm.alpha_beta_pruning import alpha_beta_pruning
from algorithm.minimax import minimax
from algorithm.iddfs import iddfs

# Initialize Pygame
pygame.init()
pygame.font.init()

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Color definitions
BG_COLOR = (240, 248, 255)  # Light Alice Blue
TITLE_COLOR = (255, 255, 255)  # Royal Blue
BUTTON_NORMAL = (135, 206, 235)  # Sky Blue
BUTTON_HOVER = (70, 130, 180)  # Steel Blue
TEXT_NORMAL = (255, 255, 255)  # White
TEXT_HOVER = (245, 245, 220)  # Beige

FONT = pygame.font.Font(None, 40)
HOVER_FONT = pygame.font.Font(None, 44)


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

def draw_menu(selected_option):
    """Draws an interactive menu screen for AI selection."""
    if BACKGROUND_IMAGE:
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        WIN.fill(BG_COLOR)
    
    # Semi-transparent overlay for better text readability
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 100))  # Gray with alpha
    WIN.blit(overlay, (0, 0))
    
    # Menu title
    title_text = FONT.render("Checkers Game", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    WIN.blit(title_text, title_rect)

    # Subtitle
    subtitle_text = FONT.render("Select an Algorithm", True, TITLE_COLOR)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    WIN.blit(subtitle_text, subtitle_rect)

    # Button properties
    button_width = 400
    button_height = 70
    button_spacing = 30
    total_height = (button_height * 3) + (button_spacing * 2)
    start_y = (HEIGHT - total_height) // 2
    
    # Button rectangles and texts
    options = [
        ("1. Minimax", minimax),
        ("2. Alpha-Beta Pruning", alpha_beta_pruning),
        ("3. Iterative Deepening DFS", iddfs)
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
        shadow_rect = pygame.Rect(button_x + 5, button_y + 5, button_width, button_height)
        pygame.draw.rect(WIN, (100, 100, 100, 50), shadow_rect, border_radius=15)
        
        if is_hovered or selected_option == i:
            pygame.draw.rect(WIN, BUTTON_HOVER, button_rect, border_radius=15)
            text_surface = HOVER_FONT.render(text, True, TEXT_HOVER)
        else:
            pygame.draw.rect(WIN, BUTTON_NORMAL, button_rect, border_radius=15)
            text_surface = FONT.render(text, True, TEXT_NORMAL)
            
        text_rect = text_surface.get_rect(center=button_rect.center)
        WIN.blit(text_surface, text_rect)
    
    pygame.display.update()
    return button_rects

def select_algorithm():
    """Allows the user to select an AI algorithm with an interactive menu."""
    selected_option = None
    button_rects = None
    
    while selected_option is None:
        button_rects = draw_menu(selected_option)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_option = i
                        break
                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_option = 0
                elif event.key == pygame.K_2:
                    selected_option = 1
                elif event.key == pygame.K_3:
                    selected_option = 2
    
    algorithms = [minimax, alpha_beta_pruning, iddfs]
    return algorithms[selected_option]

def show_end_message(winner):
    """Display game over screen with winner information."""
    if BACKGROUND_IMAGE:
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
    else:
        WIN.fill(BG_COLOR)
    
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((50, 50, 50, 100))
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
    
    winner_surface = HOVER_FONT.render(winner_text, True, color)
    winner_rect = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    WIN.blit(winner_surface, winner_rect)
    
    instruction_surface = FONT.render("Press any key to close", True, TEXT_NORMAL)
    instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
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
    ai_algorithm = select_algorithm()
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = ai_algorithm(game.get_board(), 3, WHITE, game)
            if new_board:
                game.ai_move(new_board)

        winner = game.winner()
        if winner is not None:
            print(f"Winner: {winner}")
            game.update()  # Ensure final state is shown
            show_end_message(winner)
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