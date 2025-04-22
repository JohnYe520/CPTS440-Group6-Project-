from boardState import BoardState
from shortMoveWallPlace import ShortestPathAgent

# Test cases for the ShortestPathAgent with strategic wall-placement logic

def run_test(agent_start, agent_goal, opponent_start, opponent_goal, description):
    print(f"\nTest: {description}")
    print(f"Agent starts: {agent_start}, Agent goal: {agent_goal}")
    print(f"Opponent starts: {opponent_start}, Opponent goal: {opponent_goal}\n")

    board = BoardState(size=9)
    agent = ShortestPathAgent(board, player_num=2, start_pos=agent_start, goal_pos=agent_goal,
                              opponent_start=opponent_start, opponent_goal=opponent_goal)
    agent.move_shortest_path(max_steps=50)

if __name__ == '__main__':
    # Test Case 1: Direct opposite positions, minimal initial distance
    run_test(
        agent_start=(8, 4), agent_goal=(0, 4),
        opponent_start=(0, 4), opponent_goal=(8, 4),
        description="Direct opposite positions, straightforward race"
    )

    # Test Case 2: Diagonal opposite corners, more complex pathfinding required
    run_test(
        agent_start=(8, 8), agent_goal=(0, 0),
        opponent_start=(0, 0), opponent_goal=(8, 8),
        description="Diagonal opposite corners, longer paths"
    )

    # Test Case 3: Same column but closer to center, high likelihood of wall interaction
    run_test(
        agent_start=(8, 2), agent_goal=(0, 2),
        opponent_start=(0, 2), opponent_goal=(8, 2),
        description="Same column, potential frequent wall placements"
    )
