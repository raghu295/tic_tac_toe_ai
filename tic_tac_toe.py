import pygame
import sys

# Initialize pygame
pygame.init()

# Define the size of the board
WIDTH, HEIGHT = 400, 400
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Define colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BG_COLOR)

# Game board
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Define the AI and human player
HUMAN = 'O'
AI = 'X'

# Draw the grid lines
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

draw_lines()

# Mark the square on the board
def mark_square(row, col, player):
    board[row][col] = player
    if player == HUMAN:
        pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
    elif player == AI:
        pygame.draw.line(screen, CROSS_COLOR, 
                         (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                         (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, 
                         (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                         (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Check if the square is empty
def is_empty_square(row, col):
    return board[row][col] is None

# Check if the board is full
def is_board_full():
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

# Check for win conditions
def check_win(player):
    for row in range(BOARD_ROWS):
        if board[row] == [player, player, player]:
            return True

    for col in range(BOARD_COLS):
        if [board[row][col] for row in range(BOARD_ROWS)] == [player, player, player]:
            return True

    if [board[i][i] for i in range(BOARD_ROWS)] == [player, player, player]:
        return True

    if [board[i][BOARD_ROWS - i - 1] for i in range(BOARD_ROWS)] == [player, player, player]:
        return True

    return False

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(AI):
        return 1
    if check_win(HUMAN):
        return -1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if is_empty_square(row, col):
                    board[row][col] = AI
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if is_empty_square(row, col):
                    board[row][col] = HUMAN
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# AI makes a move
def ai_move():
    best_score = -float('inf')
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if is_empty_square(row, col):
                board[row][col] = AI
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        mark_square(move[0], move[1], AI)

# Main game loop
def main():
    running = True
    player_turn = HUMAN

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn == HUMAN:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if is_empty_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, HUMAN)
                    if check_win(HUMAN):
                        print('Human wins!')
                        running = False
                    elif is_board_full():
                        print('Draw!')
                        running = False
                    player_turn = AI

            if player_turn == AI and running:
                pygame.time.wait(500)  # Delay for AI's turn (optional)
                ai_move()
                if check_win(AI):
                    print('AI wins!')
                    running = False
                elif is_board_full():
                    print('Draw!')
                    running = False
                player_turn = HUMAN

        pygame.display.update()

if __name__ == '__main__':
    main()
