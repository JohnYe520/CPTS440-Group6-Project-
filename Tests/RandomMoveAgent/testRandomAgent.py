import json
import time
import copy
import random
import os
from boardState import BoardState
from aStarAgent import AStarAgent
#from bfsAgent import BFSAgent
from randomMove import RandomMoveAgent

# --------------------------------------------------------------
# This is the implementation for testing the A* agent with the BFS agent.
# Starting location for each agent are randomized in this test, total 100 games will be run 
# The result are logged to a JSON file shortRandomTest.json that will be save in the same directory with this test file
# --------------------------------------------------------------

# Checks if the specified player has reached their goal row.
def is_goal_reached(board_state, player_num):
    # Added check for player existence
    if player_num - 1 >= len(board_state.players) or board_state.players[player_num - 1] is None:
        return False
    player = board_state.players[player_num - 1]
    if player_num == 1:
        return player.Y == board_state.size - 1
    else:
        return player.Y == 0

# Run a game between A* Agent and RandomMoveAgent Agent with randomized starting positions
def run_game(game_id, max_turns=100):
    print(f"\n--- Starting Game {game_id} ---")
    start_time = time.time()

    # Initialize board
    board = BoardState(size=9) # Use standard 9x9 board

    # Check if players list is populated correctly by BoardState init
    if len(board.players) < 2:
        print(f"Error: BoardState did not initialize players correctly for Game {game_id}.")
        return None

    # Remove default players placed by BoardState init first
    if board.players[0] is not None:
         if 0 <= board.players[0].Y < board.size and 0 <= board.players[0].X < board.size:
              board.board[board.players[0].Y, board.players[0].X].remove_player()
    if board.players[1] is not None:
         if 0 <= board.players[1].Y < board.size and 0 <= board.players[1].X < board.size:
              board.board[board.players[1].Y, board.players[1].X].remove_player()

    # Choose random columns for starting positions
    start_col_p1 = random.randint(0, board.size - 1)
    start_col_p2 = random.randint(0, board.size - 1)

    # Place players at random starting positions
    board.teleport_player(1, 0, start_col_p1)
    board.teleport_player(2, board.size - 1, start_col_p2)

    print(f"Game {game_id}: P1 starts at (0, {start_col_p1}), P2 starts at ({board.size - 1}, {start_col_p2})")

    # Initialize agents
    agent1 = AStarAgent(player_num=1)
    agent2 = RandomMoveAgent(player_num=2)
    agents = {1: agent1, 2: agent2}
    current_player_num = 1

    # Initialize game log with actual starting positions
    game_log = {
        "game_id": game_id,
        "winner": None,
        "reason": None,
        "turns": 0,
        "player1_path": [(board.players[0].Y, board.players[0].X)],
        "player2_path": [(board.players[1].Y, board.players[1].X)],
        "astar_wall_placements": [],
        "time_seconds": 0.0
    }

    # Main Game Loop
    for turn in range(max_turns * 2):
        player_turn = (turn % 2) + 1
        agent = agents[player_turn]

        # Check win condition before agent moves
        if is_goal_reached(board, player_turn):
            game_log["winner"] = player_turn
            game_log["reason"] = "Goal Reached"
            print(f"Game {game_id}: Player {player_turn} wins on turn {game_log['turns']}.")
            break

        # Get action from the current agent
        board_copy = copy.deepcopy(board)
        action, params = agent.choose_action(board_copy)
        del board_copy

        # Execute action
        action_taken = False
        if action == "move_jumpaware":
            y, x = params["target"]
            if 0 <= y < board.size and 0 <= x < board.size:
                 target_space = board.board[y][x]
                 if target_space.player is None or target_space.player == agent.player_num:
                    board.teleport_player(agent.player_num, y, x)
                    action_taken = True
                 else:
                     print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Invalid move_jumpaware to {params['target']}. Target occupied by Player: {target_space.player}")
            else:
                 print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Invalid move_jumpaware (out of bounds): {params['target']}")

        elif action == "wall":
            if isinstance(agent, AStarAgent):
                c1 = params["corner1"]
                c2 = params["corner2"]
                direction = params["direction"]
                if board.place_wall(c1, c2, direction):
                    game_log["astar_wall_placements"].append({
                        "turn": game_log['turns'],
                        "corner1": c1,
                        "corner2": c2,
                        "direction": direction
                    })
                    action_taken = True
                else:
                     print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Failed wall placement: {params}")
            else:
                print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Attempted illegal wall placement: {params}")


        elif action == "move":
             direction = params["direction"]
             y, x = board.players[agent.player_num - 1].Y, board.players[agent.player_num - 1].X
             current_space = board.board[y][x]
             walls = current_space.get_walls()
             if walls[direction] == 0:
                 dy, dx = [(-1, 0), (0, 1), (1, 0), (0, -1)][direction]
                 ny, nx = y + dy, x + dx
                 if 0 <= ny < board.size and 0 <= nx < board.size:
                     target_space = board.board[ny][nx]
                     if target_space.player is None:
                         board.move_player(agent.player_num, direction)
                         action_taken = True
                     else:
                         print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Invalid move to {(ny, nx)}. Target occupied by Player: {target_space.player}")
                 else:
                     print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Invalid move (out of bounds): {direction}")
             else:
                 print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Invalid move (wall): {direction}")


        elif action == "noop":
            action_taken = True
            pass

        # Log position after action
        if action_taken:
            current_pos = (board.players[player_turn - 1].Y, board.players[player_turn - 1].X)
            path_list = game_log[f"player{player_turn}_path"]
            if not path_list or path_list[-1] != current_pos:
                path_list.append(current_pos)
        elif action != "noop":
             print(f" T{game_log['turns']}.{player_turn}: P{player_turn} ({type(agent).__name__}) - Action {action} FAILED or caused error. Turn skipped.")


        # Increment turn counter only after player 2 has moved
        if player_turn == 2:
            game_log["turns"] += 1

        # Check for win condition again after moving
        if is_goal_reached(board, player_turn):
            game_log["winner"] = player_turn
            game_log["reason"] = "Goal Reached"
            print(f"Game {game_id}: Player {player_turn} wins on turn {game_log['turns']}.")
            break

    # Draw condition with no winner
    if game_log["winner"] is None:
        game_log["reason"] = f"Max turns ({max_turns}) reached"
        game_log["winner"] = "Draw"
        print(f"Game {game_id}: Draw after {max_turns} turns.")

    end_time = time.time()
    game_log["time_seconds"] = round(end_time - start_time, 4)
    print(f"Game {game_id} finished in {game_log['time_seconds']:.4f} seconds.")

    return game_log

if __name__ == "__main__":
    num_games = 100
    all_game_results = []

    for i in range(1, num_games + 1):
        result = run_game(game_id=i, max_turns=100)
        if result is not None:
            all_game_results.append(result)
        else:
            print(f"Skipping results for Game {i} due to setup error.")


    # Log the result to a JSON file and store it in the same directory with this file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "shortRandomTest.json"
    output_filename = os.path.join(output_dir, file_name)

    print(f"\nAttempting to write results to: {output_filename}")

    try:
        with open(output_filename, 'w') as f:
            json.dump(all_game_results, f, indent=4)
            print(f"\nResults for {len(all_game_results)} games saved to {output_filename}")
    except IOError as e:
        print(f"\nIOError writing results to {output_filename}: {e}")
        print("Please check the path exists and you have write permissions in that directory.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during file writing: {e}")


    # Print out the win rate for each agent
    p1_wins = sum(1 for result in all_game_results if result["winner"] == 1)
    p2_wins = sum(1 for result in all_game_results if result["winner"] == 2)
    draws = sum(1 for result in all_game_results if result["winner"] == "Draw")
    total_games = len(all_game_results)

    p1_winrate = (p1_wins / total_games) * 100
    p2_winrate = (p2_wins / total_games) * 100
    draw_rate = (draws / total_games) * 100

    print(f"\n--- Summary ---")
    print(f"Total Games: {total_games}")
    print(f"Player 1 (AStarAgent) Wins: {p1_wins} ({p1_winrate:.2f}%)")
    print(f"Player 2 (RandomMoveAgent) Wins: {p2_wins} ({p2_winrate:.2f}%)")
    print(f"Draws: {draws} ({draw_rate:.2f}%)")
