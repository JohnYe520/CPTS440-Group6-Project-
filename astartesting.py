from boardState import BoardState
from astarpathfinding import a_star_path

def print_found(path):
    if path is None:
        print("\nNo path found")
    else:
        print("\nFound a path:")
        print("\n->".join(f"({r},{c})" for r, c in path))

def visualize_path(board: BoardState, path):
    size = board.size
    path_set = set(path if path else [])

    def cell_content(r, c):
        state = board.board[r][c]
        val = state.player
        if val == 1:
            return "1"
        elif val == 2:
            return "2"
        elif (r, c) in path_set:
            return "*"
        return "."

    print("\nBoard with Path and Walls:\n")

    for r in range(size):
        # Row of cells with vertical walls
        row = ""
        for c in range(size):
            cell = f" {cell_content(r, c)} "
            east_wall = board.board[r][c].get_walls()[1]
            row += cell + ("|" if east_wall else " ")
        print(row)

        # Row of horizontal walls
        if r < size - 1:
            wall_row = ""
            for c in range(size):
                south_wall = board.board[r][c].get_walls()[2]
                wall_row += "---+" if south_wall else "   +"
            print(wall_row)


def test_basic_path():
    print("\nPerforming Basic Path Test:")
    board = BoardState(size=5)
    path1 = a_star_path(board, 1)
    path2 = a_star_path(board, 2)

    print("\nPlayer 1:")
    print_found(path1)
    visualize_path(board, path1)
    print("\nPlayer 2:")
    print_found(path2)
    visualize_path(board, path2)

def test_with_wall():
    print("\n\nPerforming path with wall test:")
    board = BoardState(size=5)
    board.place_wall((1,1), (2,2), 0)
    path1 = a_star_path(board, 1)

    print("\nPlayer1:")
    print_found(path1)
    visualize_path(board, path1)

def test_complex_walls():
    print("\n\nPerforming complex wall test:")
    board = BoardState(size = 5)

    board.place_wall((0, 1), (1, 2), 0)
    board.place_wall((1, 1), (2, 2), 1)
    board.place_wall((2, 1), (3, 2), 0)
    board.place_wall((3, 1), (4, 2), 1)

    path1 = a_star_path(board, 1)
    print("\nPlayer 1:")
    print_found(path1)
    visualize_path(board, path1)

def test_no_path():
    print("\n\nPerforming no path test:")
    board = BoardState(size=3)

    #blocking entire horizontal
    board.place_wall((0, 0), (1, 1), 0)
    board.place_wall((0, 1), (1, 2), 0)
    board.place_wall((1, 0), (2, 1), 0)
    board.place_wall((1, 1), (2, 2), 0)


    path1 = a_star_path(board, 1)
    print("\nPlayer 1:")
    print_found(path1)

def test_jump_opponent():
    print("\n\nPerforming jump opponent test:")
    board = BoardState(size = 5)

    board.teleport_player(1, 2, 2)  # P1 to (2,2)
    board.teleport_player(2, 3, 2)  # P2 to (3,2)

    print(f"Player 1 at: ({board.players[0].Y}, {board.players[0].X})")
    print(f"Player 2 at: ({board.players[1].Y}, {board.players[1].X})")

    path1 = a_star_path(board, 1)

    print("\nPlayer 1:")
    print_found(path1)
    visualize_path(board, path1)

def test_sidestep_opponent():
    print("\n\nPerforming sidestep opponent test:")
    board = BoardState(size=5)
    board.move_player(1,2)
    board.move_player(2, 0)
    board.move_player(1, 2)
    board.move_player(2, 0)
    board.move_player(2, 2)
    board.place_wall((3, 2), (4,3), 0)

    path1 = a_star_path(board, 1)
    board._BoardState__set_player([2,2], 1)
    print("\nPlayer 1:")
    print_found(path1)
    visualize_path(board, path1)

if __name__ == "__main__":
    test_basic_path()
    test_with_wall()
    test_complex_walls()
    test_no_path()
    test_jump_opponent()
    test_sidestep_opponent()