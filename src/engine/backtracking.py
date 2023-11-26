import numpy as np


def possibility(puzzle, num, i, j):
    # getting indices of the top left square in relevant block
    block_i = 3 * (i // 3)  # row index
    block_j = 3 * (j // 3)  # column index

    # variables to determine if num is in the row, column or block
    in_row = num in puzzle[i]
    in_col = num in puzzle[:, j]
    in_block = num in puzzle[block_i : block_i + 3, block_j : block_j + 3]

    # return True if num is not in row, col or block
    return not in_row and not in_col and not in_block


def backtracker(puzzle):
    # check puzzle is numpy array with shape (9,9)
    assert isinstance(puzzle, np.ndarray) and puzzle.shape == (9, 9)

    puzzle = puzzle.copy()

    def solve(puzzle):
        for i in range(9):  # iterate over rows
            for j in range(9):  # iterate over columns
                if puzzle[i][j] == 0:  # find an empty cell
                    # introduce randomness so backtracking is not deterministic
                    numbers = np.arange(1, 10)
                    np.random.shuffle(numbers)

                    for num in numbers:  # try all numbers from 1 to 9
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
