import pygame
from boardState import BoardState

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 60
MARGIN = 20
BOARD_SIZE = 9
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE + MARGIN * 2
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board Game")
clock = pygame.time.Clock()

# Initialize game board
board = BoardState(size=BOARD_SIZE)
selected_corner = None
current_player = 1  # Player 1 starts

def draw_board():
    screen.fill(WHITE)
    
    # Draw the grid (light gray lines)
    for r in range(board.size + 1):
        pygame.draw.line(
            screen, GRAY,
            (MARGIN, MARGIN + r * CELL_SIZE),
            (MARGIN + board.size * CELL_SIZE, MARGIN + r * CELL_SIZE),
            1
        )
    for c in range(board.size + 1):
        pygame.draw.line(
            screen, GRAY,
            (MARGIN + c * CELL_SIZE, MARGIN),
            (MARGIN + c * CELL_SIZE, MARGIN + board.size * CELL_SIZE),
            1
        )
    
    # Draw walls (thick black lines)
    for r in range(board.size):
        for c in range(board.size):
            x = MARGIN + c * CELL_SIZE
            y = MARGIN + r * CELL_SIZE
            walls, val = board.board[r, c]
            if walls[0]:  # North wall
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 3)
            if walls[1]:  # East wall
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 3)
            if walls[2]:  # South wall
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 3)
            if walls[3]:  # West wall
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 3)
            
            # Draw players
            if val == 1:
                pygame.draw.circle(screen, RED, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//3)
            elif val == 2:
                pygame.draw.circle(screen, BLUE, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//3)

def handle_movement(direction):
    global current_player
    try:
        board.move_player(current_player, direction)
        current_player = 2 if current_player == 1 else 1  # Switch player
    except Exception as e:
        print(f"Invalid move: {e}")

def handle_wall_placement(corner1, corner2, direction):
    if board.place_wall(corner1, corner2, direction):
        print("Wall placed successfully")
    else:
        print("Invalid wall placement")

running = True
placing_wall = False
corners = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Movement with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                handle_movement(0)
            elif event.key == pygame.K_RIGHT:
                handle_movement(1)
            elif event.key == pygame.K_DOWN:
                handle_movement(2)
            elif event.key == pygame.K_LEFT:
                handle_movement(3)
        
        # Wall placement with mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            c = (x - MARGIN) // CELL_SIZE
            r = (y - MARGIN) // CELL_SIZE
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                corners.append((r, c))
                if len(corners) == 2:
                    # Determine direction (0 for horizontal, 1 for vertical)
                    if abs(corners[0][0] - corners[1][0]) == 1:
                        direction = 1  # Vertical
                    else:
                        direction = 0  # Horizontal
                    handle_wall_placement(corners[0], corners[1], direction)
                    corners = []

    draw_board()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()