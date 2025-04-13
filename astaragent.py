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
            return("move_jumpaware", {"target": next_pos})
        else:
            if len(opp_path) > 2:
                block_pos = opp_path[1]
                r, c = block_pos

                dir = random.choice([0, 1])

                if dir == 0:  # horizontal
                    if r < board_state.size - 1 and c < board_state.size - 1:
                        corner1 = (r, c)
                        corner2 = (r + 1, c + 1)
                        return ("wall", {"corner1": corner1, "corner2": corner2, "direction": 0})
                else:  # vertical
                    if r < board_state.size - 1 and c < board_state.size - 1:
                        corner1 = (r, c)
                        corner2 = (r + 1, c + 1)
                        return ("wall", {"corner1": corner1, "corner2": corner2, "direction": 1})
            return("move", {"direction": 2})