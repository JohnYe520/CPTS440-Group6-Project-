from astarpathfinding import a_star_path
import random

class AStarAgent:
    def __init__(self, player_num):
        self.player_num = player_num
        self.opponent_num = 2 if player_num == 1 else 1

    def choose_action(self, board_state):
        my_path = a_star_path(board_state, self.player_num)
        opp_path = a_star_path(board_state, self.opponent_num)

        if not my_path or not opp_path:
            return ("move", {"direction": 2})
        
        my_len = len(my_path)
        opp_len = len(opp_path)

        if my_len <= opp_len:
            if len(my_path) < 2:
                print("[AStarAgent] Already at goal or no move needed.")
                return ("noop", {})
            next_pos = my_path[1]
            return ("move_jumpaware", {"target": next_pos})
        else:
            if len(opp_path) > 2:
                block_pos = opp_path[1]
                r, c = block_pos

                # Try both wall directions and return the first valid placement
                wall_attempts = [
                    (0, (r, c), (r + 1, c + 1)),  # Horizontal
                    (1, (r, c), (r + 1, c + 1))   # Vertical
                ]

                for direction, corner1, corner2 in wall_attempts:
                    # Make sure corners are within bounds
                    if corner2[0] < board_state.size and corner2[1] < board_state.size:
                        if board_state.place_wall(corner1, corner2, direction):
                            return ("wall", {"corner1": corner1, "corner2": corner2, "direction": direction})

            # Fall back to moving if wall can't be placed
            return ("move_jumpaware", {"target": my_path[1]})