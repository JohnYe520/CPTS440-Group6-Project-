import os
import json
import random
import time
from boardState import BoardState
from aStarAgent import AStarAgent

# Executes a single turn for the given agent and logs moves/walls
def run_agent_turn(agent, board_state, move_log, wall_log):
    action, params = agent.choose_action(board_state)

    if action == "noop":
        return
    elif action == "move":
        board_state.move_player(agent.player_num, params["direction"])
        player = board_state.players[agent.player_num - 1]
        move_log.append((player.Y, player.X))  # log position
    elif action == "move_jumpaware":
        y, x = params["target"]
        board_state.teleport_player(agent.player_num, y, x)
        move_log.append((y, x))
    elif action == "wall":
        wall_log.append((params["corner1"], params["corner2"], params["direction"]))  # log wall placement

# Runs multiple self-play games between two AStarAgents and logs results
def test_astar_winrates(num_games=100, board_size=5, turns_per_game=100):
    wins = {1: 0, 2: 0, "draw": 0}
    all_game_results = []

    for game_id in range(1, num_games + 1):
        board = BoardState(size=board_size)

        valid_positions_p1 = [(y, x) for y in range(board_size) for x in range(board_size) if y != 0 and y != board_size - 1]
        valid_positions_p2 = [(y, x) for y in range(board_size) for x in range(board_size) if y != 0 and y != board_size - 1]

        start_pos1 = random.choice(valid_positions_p1)
        start_pos2 = random.choice([pos for pos in valid_positions_p2 if pos != start_pos1])

        board.teleport_player(1, *start_pos1)
        board.teleport_player(2, *start_pos2)

        agent1 = AStarAgent(player_num=1)
        agent2 = AStarAgent(player_num=2)

        goal_row_p1 = 0 if start_pos1[0] > board_size // 2 else board_size - 1
        goal_row_p2 = 0 if start_pos2[0] > board_size // 2 else board_size - 1

        move_log_1 = [start_pos1]
        move_log_2 = [start_pos2]
        wall_log_1 = []
        wall_log_2 = []

        winner = None
        draw = False
        turns_used = 0
        start_time = time.time()

        for _ in range(turns_per_game):
            turns_used += 1
            run_agent_turn(agent1, board, move_log_1, wall_log_1)
            if board.players[0].Y == goal_row_p1:
                wins[1] += 1
                winner = 1
                break

            run_agent_turn(agent2, board, move_log_2, wall_log_2)
            if board.players[1].Y == goal_row_p2:
                wins[2] += 1
                winner = 2
                break

        # If no winner after all turns, it's a draw
        if winner is None:
            draw = True
            wins["draw"] += 1

        time_elapsed = round(time.time() - start_time, 4)

        game_result = {
            "game_id": game_id,
            "start_positions": {"P1": start_pos1, "P2": start_pos2},
            "goal_rows": {"P1": goal_row_p1, "P2": goal_row_p2},
            "move_path": {"P1": move_log_1, "P2": move_log_2},
            "wall_history": {"P1": wall_log_1, "P2": wall_log_2},
            "winner": winner,
            "draw": draw,
            "turns_used": turns_used,
            "time_spent_seconds": time_elapsed
        }

        all_game_results.append(game_result)

        # === Print per-game result to terminal ===
        print(f"\n--- Game {game_id} Result ---")
        print(f"Start Positions: P1: {start_pos1}, P2: {start_pos2}")
        print(f"Goal Rows: P1: {goal_row_p1}, P2: {goal_row_p2}")
        if draw:
            print("Result: Draw")
        else:
            print(f"Winner: Player {winner}")
        print(f"Turns used: {turns_used}, Time spent: {time_elapsed:.4f}s")
        print(f"Move path P1: {move_log_1}")
        print(f"Move path P2: {move_log_2}")
        print(f"Walls placed by P1: {wall_log_1}")
        print(f"Walls placed by P2: {wall_log_2}")

    # Save results to JSON
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "2AStarAgentsTesting.json")

    print(f"\nAttempting to write results to: {output_path}")
    try:
        with open(output_path, 'w') as f:
            json.dump(all_game_results, f, indent=4)
            print(f"Results for {len(all_game_results)} games saved to {output_path}")
    except IOError as e:
        print(f"IOError writing results to {output_path}: {e}")
        print("Please check the path exists and you have write permissions.")
    except Exception as e:
        print(f"Unexpected error during file writing: {e}")

    # Final win summary
    print("\n=== A* Agent Winrate Summary ===")
    print(f"Player 1 Wins: {wins[1]} / {num_games} ({wins[1]/num_games:.2%})")
    print(f"Player 2 Wins: {wins[2]} / {num_games} ({wins[2]/num_games:.2%})")
    print(f"Draws (Max Turn is reached): {wins['draw']} / {num_games} ({wins['draw']/num_games:.2%})")

if __name__ == "__main__":
    test_astar_winrates()
