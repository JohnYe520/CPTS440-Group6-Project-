import random
from boardState import BoardState
from aStarAgent import AStarAgent
from astartesting import visualize_path
from astarpathfinding import a_star_path

class RandomMover:
    def __init__(self, player_num):
        self.player_num = player_num

    def choose_action(self, board_state):
        directions = [0, 1, 2, 3]
        random.shuffle(directions)
        y, x = board_state.players[self.player_num - 1].Y, board_state.players[self.player_num - 1].X
        current_space = board_state.board[y][x]
        walls = current_space.get_walls()

        for d in directions:
            if walls[d] == 0:
                return ("move", {"direction": d})
            
        return ("noop", {}) #no valid moves
    
class GameManager:
    def __init__(self):
        self.board = BoardState(size=9)

        mid_col = self.board.size // 2
        self.board.teleport_player(1, 0, mid_col)
        self.board.teleport_player(2, self.board.size - 1, mid_col)

        self.player1 = AStarAgent(player_num=1)
        self.player2 = RandomMover(player_num=2)

    def is_goal_reached(self, player_num):
        player = self.board.players[player_num - 1]
        if player_num == 1:
            return player.Y == self.board.size - 1
        else:
            return player.Y == 0

    def play_game(self, max_turns=50):
        print("\n=== Starting Game ===")
        visualize_path(self.board, None)

        for turn in range(max_turns):
            print(f"\n--- Turn {turn + 1} ---")

            for agent in [self.player1, self.player2]:
                if self.is_goal_reached(agent.player_num):
                    print(f"\n🎉 Player {agent.player_num} has reached their goal!")
                    return

                action, params = agent.choose_action(self.board)
                print(f"[Turn {turn + 1}] Player {agent.player_num} chose action: {action}, {params}")

                if action == "noop":
                    continue
                elif action == "move":
                    self.board.move_player(agent.player_num, params["direction"])
                elif action == "move_jumpaware":
                    y, x = params["target"]
                    self.board.teleport_player(agent.player_num, y, x)
                elif action == "wall":
                    self.board.place_wall(params["corner1"], params["corner2"], params["direction"])

                visualize_path(self.board, a_star_path(self.board, agent.player_num))

        print("\n Game ended without a winner.")

if __name__ == "__main__":
    gm = GameManager()
    gm.play_game()