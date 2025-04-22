import pygame
import sys
from boardState import BoardState
from GameManager import GameManager
from aStarAgent import AStarAgent # Import AStarAgent for AI

# --- Constants ---
BOARD_SIZE = 9
SQUARE_SIZE = 60
WALL_THICKNESS = 8
GRID_WIDTH = BOARD_SIZE * SQUARE_SIZE + (BOARD_SIZE - 1) * WALL_THICKNESS
GRID_HEIGHT = GRID_WIDTH
INFO_HEIGHT = 50
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 180
SCREEN_WIDTH = GRID_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT + INFO_HEIGHT + BUTTON_HEIGHT + 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19) # Walls
BLUE = (0, 0, 255)   # Player 1
RED = (255, 0, 0)     # Player 2
GREEN = (0, 255, 0)   # Possible moves/highlight
YELLOW = (255, 255, 0) # Selected piece
GREY = (128, 128, 128) # Background
LIGHT_GREY = (200, 200, 200) # Button color
DARK_GREY = (100, 100, 100) # Button hover/text

# Game States
PLAYER_TURN = 1
AI_TURN = 2
GAME_OVER = 3

# Input modes
MODE_MOVE = 'move'
MODE_WALL_H = 'wall_h' # Placing horizontal wall
MODE_WALL_V = 'wall_v' # Placing vertical wall

# --- Helper Functions ---

def get_screen_coords(board_row, board_col):
    """Converts board (row, col) to screen (x, y) top-left corner"""
    x = board_col * (SQUARE_SIZE + WALL_THICKNESS)
    y = INFO_HEIGHT + board_row * (SQUARE_SIZE + WALL_THICKNESS)
    return x, y

def get_board_coords(screen_x, screen_y):
    """Converts screen (x, y) to board (row, col) if click is on a square"""
    if screen_y < INFO_HEIGHT or screen_y > INFO_HEIGHT + GRID_HEIGHT:
        return None # Clicked outside grid

    # Check click within square bounds, not the wall gaps
    col_guess = screen_x // (SQUARE_SIZE + WALL_THICKNESS)
    row_guess = (screen_y - INFO_HEIGHT) // (SQUARE_SIZE + WALL_THICKNESS)

    if 0 <= row_guess < BOARD_SIZE and 0 <= col_guess < BOARD_SIZE:
        x_start, y_start = get_screen_coords(row_guess, col_guess)
        if x_start <= screen_x < x_start + SQUARE_SIZE and \
           y_start <= screen_y < y_start + SQUARE_SIZE:
            return row_guess, col_guess
    return None # Clicked on a wall gap or outside

def get_wall_coords_from_click(screen_x, screen_y):
    """ Estimates the top-left board coords (r, c) for placing a wall based on click """
    if screen_y < INFO_HEIGHT or screen_y > INFO_HEIGHT + GRID_HEIGHT:
        return None

    # Estimate the nearest top-left corner of a 2x2 block
    col = round((screen_x - SQUARE_SIZE / 2) / (SQUARE_SIZE + WALL_THICKNESS))
    row = round(((screen_y - INFO_HEIGHT) - SQUARE_SIZE / 2) / (SQUARE_SIZE + WALL_THICKNESS))

    # Clamp to valid top-left indices for walls
    row = max(0, min(BOARD_SIZE - 2, row))
    col = max(0, min(BOARD_SIZE - 2, col))

    return row, col


def draw_button(screen, text, rect, font, active=False):
    """Draws a button"""
    color = LIGHT_GREY if not active else DARK_GREY
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, BLACK if not active else WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_board(screen, board_state: BoardState, selected_piece_pos=None, possible_moves=None, current_mode=MODE_MOVE):
    """Draws the grid, players, walls, selection, and possible moves"""
    # Draw Squares and Players
    for r in range(board_state.size):
        for c in range(board_state.size):
            x, y = get_screen_coords(r, c)
            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, WHITE, rect) # Draw square background

            # Highlight selected piece
            if selected_piece_pos == (r, c):
                pygame.draw.rect(screen, YELLOW, rect, 3) # Border highlight

            # Highlight possible moves
            if possible_moves and (r, c) in possible_moves:
                 pygame.draw.circle(screen, GREEN, rect.center, SQUARE_SIZE // 6)

            # Draw Player Pawns
            player_num = board_state.board[r, c].player
            if player_num == 1:
                pygame.draw.circle(screen, BLUE, rect.center, SQUARE_SIZE // 3)
            elif player_num == 2:
                pygame.draw.circle(screen, RED, rect.center, SQUARE_SIZE // 3)

            # Highlight potential wall placement area (visual feedback)
            if current_mode in [MODE_WALL_H, MODE_WALL_V]:
                 mx, my = pygame.mouse.get_pos()
                 hover_coords = get_wall_coords_from_click(mx, my)
                 if hover_coords:
                     hr, hc = hover_coords
                     hx, hy = get_screen_coords(hr, hc)
                     highlight_color = (200, 150, 150, 150) # Semi-transparent red
                     s = pygame.Surface((SQUARE_SIZE*2+WALL_THICKNESS, SQUARE_SIZE*2+WALL_THICKNESS), pygame.SRCALPHA)
                     s.fill(highlight_color)
                     screen.blit(s, (hx, hy))

    # Iterate through potential top-left corners for walls
    for r in range(board_state.size - 1):
        for c in range(board_state.size - 1):
            x, y = get_screen_coords(r, c) # Screen coords of top-left square (r, c)

            # Check for Horizontal Wall starting below (r, c)
            space1 = board_state.board[r, c]
            space_below1 = board_state.board[r + 1, c]
            space_right1 = board_state.board[r, c + 1]
            space_diag1 = board_state.board[r + 1, c + 1]

            # A horizontal wall exists if BOTH pairs are blocked
            is_h_wall = (space_below1 not in space1.neighbors) and \
                        (space_diag1 not in space_right1.neighbors)
                        # Add check for wall object if using them: and board_state.hWalls[r, c] is not None

            if is_h_wall:
                wall_x = x
                wall_y = y + SQUARE_SIZE
                wall_rect = pygame.Rect(wall_x, wall_y, SQUARE_SIZE * 2 + WALL_THICKNESS, WALL_THICKNESS)
                pygame.draw.rect(screen, BROWN, wall_rect)

            # Check for Vertical Wall starting right of (r, c)
            # Re-use space objects from above
            # A vertical wall exists if BOTH pairs are blocked
            is_v_wall = (space_right1 not in space1.neighbors) and \
                        (space_diag1 not in space_below1.neighbors)
                        # Add check for wall object if using them: and board_state.vWalls[r, c] is not None

            if is_v_wall:
                wall_x = x + SQUARE_SIZE
                wall_y = y
                wall_rect = pygame.Rect(wall_x, wall_y, WALL_THICKNESS, SQUARE_SIZE * 2 + WALL_THICKNESS)
                pygame.draw.rect(screen, BROWN, wall_rect)

def get_valid_moves(board_state: BoardState, player_num: int):
    """ Calculates valid moves for a player, including jumps """
    player = board_state.players[player_num - 1]
    start_pos = (player.Y, player.X)
    size = board_state.size
    move_dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)] # N, E, S, W
    valid_targets = set()

    q = [(start_pos, 0)] # Position, distance (only distance 1 needed for direct moves/jumps)
    visited = {start_pos}

    opponent_pos = (board_state.players[1 if player_num == 1 else 0].Y,
                    board_state.players[1 if player_num == 1 else 0].X)

    r, c = start_pos
    current_space = board_state.board[r, c]
    walls = current_space.get_walls()

    for dir_index, (dr, dc) in enumerate(move_dirs):
        if walls[dir_index] == 0: # Check wall in moving direction
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                neighbor_space = board_state.board[nr, nc]
                # Check wall coming back (important!)
                if board_state.board[nr,nc].get_walls()[(dir_index + 2) % 4] == 0:
                    if (nr, nc) == opponent_pos:
                        # --- Opponent Found: Check Jumps ---
                        jump_r, jump_c = nr + dr, nc + dc
                        # Check wall between opponent and jump spot
                        if neighbor_space.get_walls()[dir_index] == 0:
                             if 0 <= jump_r < size and 0 <= jump_c < size:
                                 # Check wall coming back from jump spot
                                 if board_state.board[jump_r, jump_c].get_walls()[(dir_index + 2) % 4] == 0:
                                     # Check if jump spot is empty
                                     if board_state.board[jump_r, jump_c].player is None:
                                         valid_targets.add((jump_r, jump_c))
                                         continue # Found direct jump, don't check diagonals from here

                        # --- Opponent Found: Check Diagonal Sidesteps (if jump failed/blocked) ---
                        # Check wall *behind* opponent first
                        if neighbor_space.get_walls()[dir_index] == 1: # Wall behind opponent blocks diagonal
                             pass # Cannot sidestep
                        else:
                            # Check diagonal left/right relative to move direction
                            for side_step_dir in [-1, 1]: # -1 is left, 1 is right
                                diag_dr, diag_dc = 0, 0
                                side_wall_idx_1 = 0 # Wall index from opponent pos
                                side_wall_idx_2 = 0 # Wall index from diagonal pos (coming back)

                                if dir_index % 2 == 0: # Moving N/S, sidestep E/W
                                    diag_dc = side_step_dir
                                    side_wall_idx_1 = 1 if side_step_dir == 1 else 3 # E or W from opponent
                                    side_wall_idx_2 = 3 if side_step_dir == 1 else 1 # W or E from diagonal
                                else: # Moving E/W, sidestep N/S
                                    diag_dr = side_step_dir
                                    side_wall_idx_1 = 2 if side_step_dir == 1 else 0 # S or N from opponent
                                    side_wall_idx_2 = 0 if side_step_dir == 1 else 2 # N or S from diagonal

                                # Check wall from opponent to diagonal spot
                                if neighbor_space.get_walls()[side_wall_idx_1] == 0:
                                    diag_r, diag_c = nr + diag_dr, nc + diag_dc
                                    if 0 <= diag_r < size and 0 <= diag_c < size:
                                        # Check wall from diagonal spot back to opponent
                                        if board_state.board[diag_r, diag_c].get_walls()[side_wall_idx_2] == 0:
                                             # Check if diagonal spot is empty
                                             if board_state.board[diag_r, diag_c].player is None:
                                                 valid_targets.add((diag_r, diag_c))

                    elif neighbor_space.player is None: # Normal move to empty space
                        valid_targets.add((nr, nc))

    return valid_targets


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Quoridor")
    font = pygame.font.Font(None, 30)
    info_font = pygame.font.Font(None, 36)

    # --- Game Setup ---
    game_manager = GameManager()
    board_state = game_manager.board
    # Make Player 2 the A* agent
    game_manager.player2 = AStarAgent(player_num=2) # Or RandomMover(2)

    game_state = PLAYER_TURN
    current_mode = MODE_MOVE
    selected_piece_pos = None
    possible_moves = set()
    message = "Player 1's Turn (Move)"
    winner = None

    # Button Rects
    button_y = INFO_HEIGHT + GRID_HEIGHT + 5
    move_button_rect = pygame.Rect(10, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    wall_h_button_rect = pygame.Rect(10 + BUTTON_WIDTH + 10, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    wall_v_button_rect = pygame.Rect(10 + (BUTTON_WIDTH + 10) * 2, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    # At the start, before the loop
    clock = pygame.time.Clock()
    FPS = 60 # Target frames per second

    running = True
    while running:
        if game_state == PLAYER_TURN:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if game_state == PLAYER_TURN and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    board_coords = get_board_coords(mouse_x, mouse_y)

                    # Button Clicks
                    if move_button_rect.collidepoint(mouse_x, mouse_y):
                        current_mode = MODE_MOVE
                        selected_piece_pos = None # Reset selection when changing mode
                        possible_moves = set()
                        message = "Player 1's Turn (Move)"
                    elif wall_h_button_rect.collidepoint(mouse_x, mouse_y):
                        current_mode = MODE_WALL_H
                        selected_piece_pos = None
                        possible_moves = set()
                        message = "Player 1: Place Horizontal Wall (Click Top-Left)"

                    elif wall_v_button_rect.collidepoint(mouse_x, mouse_y):
                        current_mode = MODE_WALL_V
                        selected_piece_pos = None
                        possible_moves = set()
                        message = "Player 1: Place Vertical Wall (Click Top-Left)"


                    # Board Clicks
                    elif board_coords:
                        r, c = board_coords
                        # Ensure player object exists before accessing attributes
                        player1_obj = None
                        if len(board_state.players) > 0:
                            player1_obj = board_state.players[0]
                            player1_pos = (player1_obj.Y, player1_obj.X) # Get current pos before potential move
                        else:
                            player1_pos = None # Should not happen if game setup is correct

                        if current_mode == MODE_MOVE:
                            if selected_piece_pos is None:
                                # Select Player 1's piece
                                if player1_pos and (r, c) == player1_pos:
                                    selected_piece_pos = (r, c)
                                    possible_moves = get_valid_moves(board_state, 1)
                                    message = "Player 1: Select move destination"
                                    print(f"[DEBUG] Player 1 selected at {selected_piece_pos}. Possible moves: {possible_moves}") # DEBUG
                            else:
                                # Attempt to move selected piece
                                if (r, c) in possible_moves:
                                    # --- Start Debug Prints ---
                                    print(f"[DEBUG] Attempting move from {selected_piece_pos} to {(r, c)}")
                                    if player1_pos:
                                        print(f"[DEBUG] State before teleport: Player obj at ({player1_obj.Y}, {player1_obj.X})")
                                        print(f"[DEBUG] State before teleport: Old space ({player1_pos[0]},{player1_pos[1]}) player={board_state.board[player1_pos[0], player1_pos[1]].player}")
                                        print(f"[DEBUG] State before teleport: New space ({r},{c}) player={board_state.board[r, c].player}")
                                    # --- Execute move ---
                                    board_state.teleport_player(1, r, c)
                                    # --- Check State After ---
                                    print(f"[DEBUG] State after teleport: Player obj at ({player1_obj.Y}, {player1_obj.X})")
                                    print(f"[DEBUG] State after teleport: Old space ({player1_pos[0]},{player1_pos[1]}) player={board_state.board[player1_pos[0], player1_pos[1]].player}")
                                    print(f"[DEBUG] State after teleport: New space ({r},{c}) player={board_state.board[r, c].player}")
                                    # --- End Debug Prints ---

                                    # Reset selection and check win condition
                                    selected_piece_pos = None
                                    possible_moves = set()
                                    print("[DEBUG] Checking win condition for Player 1...") # DEBUG
                                    if game_manager.is_goal_reached(1):
                                        print("[DEBUG] Player 1 reached goal!") # DEBUG
                                        winner = 1
                                        game_state = GAME_OVER
                                    else:
                                        print("[DEBUG] Switching to AI turn.") # DEBUG
                                        game_state = AI_TURN
                                        message = "Player 2's Turn (AI)"
                                else:
                                    # Clicked somewhere else, deselect
                                    print(f"[DEBUG] Clicked invalid move target {(r,c)}. Deselecting.") # DEBUG
                                    selected_piece_pos = None
                                    possible_moves = set()
                                    message = "Player 1's Turn (Move)"

                        elif current_mode in [MODE_WALL_H, MODE_WALL_V]:
                            # Attempt to place wall - use estimated top-left corner
                            wall_r, wall_c = get_wall_coords_from_click(mouse_x, mouse_y)
                            if wall_r is not None:
                                corner1 = (wall_r, wall_c)
                                corner2 = (wall_r + 1, wall_c + 1) # Diagonal corner
                                direction = 0 if current_mode == MODE_WALL_H else 1

                                # Use BoardState's place_wall validation
                                if board_state.place_wall(corner1, corner2, direction):
                                    # Wall placement successful
                                    current_mode = MODE_MOVE # Switch back to move mode
                                    if game_manager.is_goal_reached(1): # Should not happen after wall, but check
                                        winner = 1
                                        game_state = GAME_OVER
                                    else:
                                        game_state = AI_TURN
                                        message = "Player 2's Turn (AI)"
                                else:
                                    # Wall placement failed (invalid location, overlap, blocks path)
                                    print(f"[DEBUG] Clicked invalid wall target {(r,c)}. Deselecting.") # DEBUG
                                    message = "Player 1: Invalid wall placement!"
                                    current_mode = MODE_MOVE # Go back to move mode

        # --- AI Turn ---
        else:
            pygame.time.wait(1000) # Small delay to see AI move
            action, params = game_manager.player2.choose_action(board_state)
            print(f"[AI Action] Player 2 chose: {action}, {params}") # Debug print

            if action == "noop":
                pass # AI does nothing
            elif action == "move":
                # Simple move - needs validation ideally, but A* should be valid
                board_state.move_player(2, params["direction"])
            elif action == "move_jumpaware":
                 # A* gives target coords directly
                 y, x = params["target"]
                 board_state.teleport_player(2, y, x)
            elif action == "wall":
                c1 = params["corner1"]
                c2 = params["corner2"]
                direction = params["direction"]

                print(f"[AI Wall] Placement succeeded at {c1} and {c2}, direction {direction}")

            if game_manager.is_goal_reached(2):
                winner = 2
                game_state = GAME_OVER
            else:
                game_state = PLAYER_TURN
                current_mode = MODE_MOVE # Reset player mode
                message = "Player 1's Turn (Move)"


        # --- Drawing ---
        screen.fill(GREY) # Clear screen
        draw_board(screen, board_state, selected_piece_pos, possible_moves, current_mode)

        # Draw Info Text
        if game_state == GAME_OVER:
            win_text = f"Player {winner} Wins!"
            text_surface = info_font.render(win_text, True, GREEN if winner == 1 else RED)
        else:
            text_surface = info_font.render(message, True, BLACK)

        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, INFO_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # Draw Buttons (only if player's turn)
        if game_state == PLAYER_TURN:
            draw_button(screen, "Select Move", move_button_rect, font, current_mode == MODE_MOVE)
            draw_button(screen, "Place H Wall", wall_h_button_rect, font, current_mode == MODE_WALL_H)
            draw_button(screen, "Place V Wall", wall_v_button_rect, font, current_mode == MODE_WALL_V)


        pygame.display.flip()
        # --- Limit Frame Rate ---
        clock.tick(FPS) # Waits if necessary to achieve the target FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()