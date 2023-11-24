def possibility(puzzle, num, y, x):
    # getting indices of the top left square in relevant block
    block_y = 3 * (y // 3)
    block_x = 3 * (x // 3)

    # variables to determine if num is in the row, column or block
    in_row = num in puzzle[y]
    in_col = num in puzzle[:, x]
    in_block = num in puzzle[block_y : block_y + 3, block_x : block_x + 3]

    # return True if num is not in row, col or block
    return not in_row and not in_col and not in_block


def backtracker(puzzle):
    puzzle = puzzle.copy()

    def solve(puzzle):
        for i in range(9):  # iterate over rows
            for j in range(9):  # iterate over columns
                if puzzle[i][j] == 0:  # find an empty cell
                    for num in range(1, 10):  # try all numbers from 1 to 9
                        if possibility(puzzle, num, i, j):
                            puzzle[i][j] = num  # fill square if number is a possibility

                            if solve(
                                puzzle
                            ):  # recursively fill in the rest of the puzzle
                                return True

                            puzzle[i][j] = 0  # backtrack if the puzzle was not solved

                    return False  # trigger backtracking if no number is possible

        return True  # puzzle solved

    # run backtracking
    solved = solve(puzzle)

    if not solved:
        return "UNSOLVABLE"

    return puzzle
