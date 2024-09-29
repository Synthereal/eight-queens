import pygame
import sys

# Initialize pygame
pygame.init()

# Constants for the chessboard
BOARD_SIZE = 8  # 8x8 chessboard
TILE_SIZE = 80  # Tile size in pixels
BUTTON_HEIGHT = 50

# Calculate window dimensions dynamically based on board and buttons
TOTAL_BOARD_WIDTH = BOARD_SIZE * TILE_SIZE
TOTAL_BOARD_HEIGHT = BOARD_SIZE * TILE_SIZE
WINDOW_WIDTH = TOTAL_BOARD_WIDTH + 200  # Extra width for left padding and board labels
WINDOW_HEIGHT = TOTAL_BOARD_HEIGHT + 100  # Extra height for top padding and buttons

# Padding to center the board in the window
PADDING_X = (WINDOW_WIDTH - TOTAL_BOARD_WIDTH) // 2
PADDING_Y = (WINDOW_HEIGHT - TOTAL_BOARD_HEIGHT - BUTTON_HEIGHT - 20) // 2

# Button configuration
NUM_BUTTONS = 4
BUTTON_WIDTH = TOTAL_BOARD_WIDTH // NUM_BUTTONS
BUTTON_Y_POSITION = PADDING_Y + TOTAL_BOARD_HEIGHT + 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (238, 207, 161)
DARK_BROWN = (178, 138, 95)
RED = (255, 0, 0)

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Eight Queens Problem")

# Font setup
font = pygame.font.SysFont(None, 36)

# Button positions and sizes (each button shares equal width and spacing)
buttons = {
    "Finish Board": pygame.Rect(PADDING_X, BUTTON_Y_POSITION, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Reset": pygame.Rect(PADDING_X + BUTTON_WIDTH, BUTTON_Y_POSITION, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Next": pygame.Rect(PADDING_X + 2 * BUTTON_WIDTH, BUTTON_Y_POSITION, BUTTON_WIDTH, BUTTON_HEIGHT),
    "Back": pygame.Rect(PADDING_X + 3 * BUTTON_WIDTH, BUTTON_Y_POSITION, BUTTON_WIDTH, BUTTON_HEIGHT),
}

# Backtracking solution data
queen_positions = [-1 for _ in range(BOARD_SIZE)]
backtracking_steps = []
current_step = 0

def is_safe(queen_positions, row, col):
    """ Check if a queen can be placed at (row, col). """
    for i in range(row):
        if (
            queen_positions[i] == col or
            queen_positions[i] - i == col - row or
            queen_positions[i] + i == col + row
        ):
            return False
    return True

def solve_eight_queens():
    """ Solve the Eight Queens problem using backtracking and store the steps. """
    global backtracking_steps
    backtracking_steps = []  # Clear previous steps
    queen_positions = [-1 for _ in range(BOARD_SIZE)]  # Reset queen positions
    backtrack(queen_positions, 0)

def backtrack(queen_positions, row):
    """ Recursively solve the problem and save steps. """
    if row == BOARD_SIZE:
        backtracking_steps.append(queen_positions[:])
        return True
    for col in range(BOARD_SIZE):
        if is_safe(queen_positions, row, col):
            queen_positions[row] = col
            backtracking_steps.append(queen_positions[:])  # Save this step
            if backtrack(queen_positions, row + 1):
                return True
            queen_positions[row] = -1  # Backtrack
            backtracking_steps.append(queen_positions[:])  # Save backtrack step
    return False

# Draw chessboard grid
def draw_chessboard():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(window, color, pygame.Rect(PADDING_X + col * TILE_SIZE, PADDING_Y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Draw buttons
def draw_buttons():
    for label, rect in buttons.items():
        pygame.draw.rect(window, BLACK, rect)
        text = font.render(label, True, WHITE)
        window.blit(text, (rect.x + rect.width // 2 - text.get_width() // 2, rect.y + rect.height // 2 - text.get_height() // 2))

# Draw queens on the board
def draw_queens(queen_positions):
    for row in range(BOARD_SIZE):
        if queen_positions[row] != -1:
            col = queen_positions[row]
            pygame.draw.circle(window, RED, (PADDING_X + col * TILE_SIZE + TILE_SIZE // 2, PADDING_Y + row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)

# Draw row indices and queen positions
def draw_row_labels(queen_positions):
    for row in range(BOARD_SIZE):
        label = font.render(f"{queen_positions[row]}", True, BLACK)
        window.blit(label, (PADDING_X - TILE_SIZE // 2 - 20, PADDING_Y + row * TILE_SIZE + TILE_SIZE // 2 - label.get_height() // 2))

# Main loop
def main():
    global current_step, queen_positions

    solve_eight_queens()  # Precompute the solution and all steps

    while True:
        window.fill(WHITE)
        draw_chessboard()
        draw_queens(queen_positions)
        draw_row_labels(queen_positions)
        draw_buttons()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse clicks for placing queens
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if the click is inside the chessboard
                if PADDING_X < x < PADDING_X + BOARD_SIZE * TILE_SIZE and PADDING_Y < y < PADDING_Y + BOARD_SIZE * TILE_SIZE:
                    col = (x - PADDING_X) // TILE_SIZE
                    row = (y - PADDING_Y) // TILE_SIZE
                    if queen_positions[row] == -1:  # Place queen in the row if none is present
                        queen_positions[row] = col
                    else:
                        queen_positions[row] = -1  # Remove queen if clicked again

                # Check if any button is clicked
                for label, rect in buttons.items():
                    if rect.collidepoint(x, y):
                        if label == "Reset":
                            queen_positions = [-1 for _ in range(BOARD_SIZE)]  # Reset board
                            current_step = 0  # Reset step counter
                        elif label == "Finish Board":
                            queen_positions = backtracking_steps[-1][:]  # Solve the board instantly
                            current_step = len(backtracking_steps) - 1
                        elif label == "Next" and current_step < len(backtracking_steps) - 1:
                            current_step += 1
                            queen_positions = backtracking_steps[current_step][:]
                        elif label == "Back" and current_step > 0:
                            current_step -= 1
                            queen_positions = backtracking_steps[current_step][:]

        pygame.display.update()

if __name__ == "__main__":
    main()