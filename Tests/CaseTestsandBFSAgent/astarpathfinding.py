import heapq

def a_star_path(board_state, player_num: int):
    size = board_state.size

    # Selecting player to get start pos and goal row
    if player_num == 1:
        start = (board_state.players[0].Y,board_state.players[0].X)
        goal_rows = {size - 1}
    elif player_num == 2:
        start = (board_state.players[1].Y,board_state.players[1].X)
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
        state = board_state.board[r][c]
        walls = state.get_walls()
        result = []

        if player_num == 1:
            opponent_position = (board_state.players[1].Y, board_state.players[1].X)
        else:
            opponent_position = (board_state.players[0].Y, board_state.players[0].X)

        for dir_index, (dr, dc) in enumerate(move_dirs):
            if walls[dir_index] == 0:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    state2 = board_state.board[nr][nc]
                    opp_wall = state2.get_walls()
                    opposite = (dir_index + 2) % 4

                    if opp_wall[opposite] == 0:
                        if (nr, nc) == opponent_position:
                            # Attempt to jump over opponent
                            jnr, jnc = nr + dr, nc + dc
                            if 0 <= jnr < size and 0 <= jnc < size:
                                jump_cell = board_state.board[jnr][jnc]
                                if opp_wall[dir_index] == 0 and jump_cell.player is None:
                                    result.append((jnr, jnc))
                                    continue

                            # If jump blocked, try sidestep (diagonal) moves
                            if dir_index in (0, 2):  # North/South
                                for dc2 in [-1, 1]:
                                    side_r, side_c = nr, nc + dc2
                                    if 0 <= side_c < size:
                                        if opp_wall[1 if dc2 == 1 else 3] == 0:
                                            side_cell = board_state.board[side_r][side_c]
                                            side_walls = side_cell.get_walls()
                                            if side_walls[(1 if dc2 == 1 else 3 + 2) % 4] == 0:
                                                result.append((side_r, side_c))
                            else:  # East/West
                                for dr2 in [-1, 1]:
                                    side_r, side_c = nr + dr2, nc
                                    if 0 <= side_r < size:
                                        if opp_wall[0 if dr2 == -1 else 2] == 0:
                                            side_cell = board_state.board[side_r][side_c]
                                            side_walls = side_cell.get_walls()
                                            if side_walls[(0 if dr2 == -1 else 2 + 2) % 4] == 0:
                                                result.append((side_r, side_c))
                        else:
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
        
    