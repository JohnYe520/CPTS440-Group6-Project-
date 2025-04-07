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

placing_wall = False
corners = []
pending_wall = None  # Wait for direction keypress ('H' or 'V')

def draw_board():
    screen.fill(WHITE)

    # Draw the grid
    for r in range(board.size + 1):
        pygame.draw.line(screen, GRAY,
                         (MARGIN, MARGIN + r * CELL_SIZE),
                         (MARGIN + board.size * CELL_SIZE, MARGIN + r * CELL_SIZE), 1)
    for c in range(board.size + 1):
        pygame.draw.line(screen, GRAY,
                         (MARGIN + c * CELL_SIZE, MARGIN),
                         (MARGIN + c * CELL_SIZE, MARGIN + board.size * CELL_SIZE), 1)

    # Draw walls and players
    for r in range(board.size):
        for c in range(board.size):
            x = MARGIN + c * CELL_SIZE
            y = MARGIN + r * CELL_SIZE
            walls, val = board.board[r, c]
            if walls[0]:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 3)
            if walls[1]:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 3)
            if walls[2]:
                pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 3)
            if walls[3]:
                pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), 3)
            if val == 1:
                pygame.draw.circle(screen, RED, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//3)
            elif val == 2:
                pygame.draw.circle(screen, BLUE, (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//3)

def handle_movement(direction):
    global current_player
    try:
        board.move_player(current_player, direction)
        current_player = 2 if current_player == 1 else 1
    except Exception as e:
        print(f"Invalid move: {e}")

def handle_wall_placement(corner1, corner2, direction):
    if board.place_wall(corner1, corner2, direction):
        print("Wall placed successfully")
    else:
        print("Invalid wall placement")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                handle_movement(0)
            elif event.key == pygame.K_RIGHT:
                handle_movement(1)
            elif event.key == pygame.K_DOWN:
                handle_movement(2)
            elif event.key == pygame.K_LEFT:
                handle_movement(3)
            elif event.key == pygame.K_h and pending_wall:
                handle_wall_placement(pending_wall[0], pending_wall[1], 0)
                pending_wall = None
            elif event.key == pygame.K_v and pending_wall:
                handle_wall_placement(pending_wall[0], pending_wall[1], 1)
                pending_wall = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            c = (x - MARGIN) // CELL_SIZE
            r = (y - MARGIN) // CELL_SIZE
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                corners.append((r, c))
                if len(corners) == 2:
                    r1, c1 = corners[0]
                    r2, c2 = corners[1]
                    if abs(r1 - r2) == 1 and abs(c1 - c2) == 1:
                        pending_wall = (corners[0], corners[1])
                        print("Select wall direction: press 'H' for horizontal or 'V' for vertical")
                    else:
                        print("Invalid corner selection — must be diagonally adjacent.")
                    corners = []

    draw_board()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
