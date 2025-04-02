import heapq

def a_star_path(board_state, player_num: int):
    size = board_state.size

    # Selecting player to get start pos and goal row
    if player_num == 1:
        start = tuple(board_state.player1[0])
        goal_rows = {size - 1}
    elif player_num == 2:
        start = tuple(board_state.player2[0])
        goal_rows = {0}
    else:
        raise ValueError("Invalid player number (should be 1 or 2)")
    
    # Adding valid move directions
    move_dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def heuristic(pos):
        # utilizing manhattan distance.
        if player_num == 1:
            return abs(size - 1 - pos[0])
        else:
            return abs(pos[0])
        
    def neighbors(pos):
        r, c = pos
        walls, _ = board_state.board[r][c]
        
        result = []
        for dir_index, (dr, dc) in enumerate(move_dirs):
            if walls[dir_index] == 0:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    opp_wall, _ = board_state.board[nr][nc]
                    # checking oposite wall
                    opposite = (dir_index + 2) % 4
                    if opp_wall[opposite] == 0:
                        result.append((nr, nc))
        return result
    
    frontier = []
    heapq.heappush(frontier, (heuristic(start), 0, start))
    came_from = {start:None}
    cost_so_far = {start:0}

    while frontier:
        _, cost, current = heapq.heappop(frontier)

        if current[0] in goal_rows:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
            
        for next_pos in neighbors(current):
            new_cost = cost + 1
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos)
                heapq.heappush(frontier, (priority, new_cost, next_pos))
                came_from[next_pos] = current

    #No Path Found
    return None
        
    