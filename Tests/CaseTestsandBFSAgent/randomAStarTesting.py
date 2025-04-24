import random
from boardState import BoardState
from aStarAgent import AStarAgent

# Executes one turn for the given agent
def run_agent_turn(agent, board_state):
    action, params = agent.choose_action(board_state)

    if action == "noop":
        return
    elif action == "move":
        board_state.move_player(agent.player_num, params["direction"])
    elif action == "move_jumpaware":
        y, x = params["target"]
        board_state.teleport_player(agent.player_num, y, x)
    elif action == "wall":
        c1 = params["corner1"]
        c2 = params["corner2"]
        dir = params["direction"]
        board_state.place_wall(c1, c2, dir)

# Simulates multiple games and calculates winrates for both A* agents
def test_astar_winrates(num_games=100, board_size=5, turns_per_game=50):
    wins = {1: 0, 2: 0}

    for game_id in range(1, num_games + 1):
        board = BoardState(size=board_size)

        # Generate valid starting positions, avoiding goal rows
        valid_positions_p1 = [(y, x) for y in range(board_size) for x in range(board_size) if y != board_size - 1]
        valid_positions_p2 = [(y, x) for y in range(board_size) for x in range(board_size) if y != 0]

        # Randomize positions, making sure they don't overlap
        start_pos1 = random.choice(valid_positions_p1)
        start_pos2 = random.choice([pos for pos in valid_positions_p2 if pos != start_pos1])

        # Set players on the board
        board.teleport_player(1, *start_pos1)
        board.teleport_player(2, *start_pos2)

        # Create agents
        agent1 = AStarAgent(player_num=1)
        agent2 = AStarAgent(player_num=2)

        for _ in range(turns_per_game):
            run_agent_turn(agent1, board)
            if board.players[0].Y == board_size - 1:
                wins[1] += 1
                break

            run_agent_turn(agent2, board)
            if board.players[1].Y == 0:
                wins[2] += 1
                break

    # Print final results
    print("\n=== A* Agent Winrate Summary ===")
    print(f"Player 1 Wins: {wins[1]} / {num_games} ({wins[1]/num_games:.2%})")
    print(f"Player 2 Wins: {wins[2]} / {num_games} ({wins[2]/num_games:.2%})")

if __name__ == "__main__":
    test_astar_winrates()
