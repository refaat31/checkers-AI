from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255,255,255)

def minimax(position,depth,max_player,game):
    if depth == 0  or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval=float('-inf')
        best_move=None
        for move in get_all_moves(position, WHITE,game):
            evaluation=minimax(move,depth-1,False,game)[0]
            maxEval=max(maxEval,evaluation)
            if maxEval==evaluation:
                best_move=move
        return maxEval,best_move
    else:
        minEval=float('inf')
        best_move=None
        for move in get_all_moves(position, RED,game):
            evaluation=minimax(move,depth-1,True,game)[0]
            minEval=min(minEval,evaluation)
            if minEval==evaluation:
                best_move=move
        return minEval,best_move

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
            draw_moves(game)
            temp_board = deepcopy(board)
            temp_piece=temp_board.get_piece(piece.row,piece.col)
            new_board= simulate_move(temp_piece,move,temp_board,game,skip)
            moves.append(new_board)
    return moves

# def draw_moves(game, board):
#     #board.draw(game.win)
#     pygame.draw.circle(game.win, (0,255,0), (280, 280), 50, 5)
#     pygame.display.update()
#     #pygame.time.delay(100)

def draw_moves(game):
    font = pygame.font.Font(None, 36)  # Create a font object (None for default font, 36 is the size)
    text = font.render("Thinking", True, (0, 255, 0))  # Render the text with an antialiasing flag and a color
    text_rect = text.get_rect(center=(280, 280))  # Center the text at (280, 280)
    game.win.blit(text, text_rect)  # Draw the text on the screen
    pygame.display.update()  # Update the display
