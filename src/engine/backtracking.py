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


def backtracker(puzzle, num_solutions=1):
    # check puzzle is numpy array with shape (9,9)
    assert isinstance(puzzle, np.ndarray) and puzzle.shape == (9, 9)

    puzzle = puzzle.copy()
    solutions = []

    def solve(puzzle, solutions):
        # break recursion when we have found enough solutions
        if len(solutions) >= num_solutions:
            return

        for i in range(9):  # iterate over rows
            for j in range(9):  # iterate over columns
                if puzzle[i][j] == 0:  # find an empty cell
                    numbers = np.arange(1, 10)
                    np.random.shuffle(numbers)  # introduce randomness

                    for n in numbers:
                        if possibility(puzzle, n, i, j):
                            puzzle[i][j] = n  # fill square if number is a possibility
                            solve(puzzle, solutions)  # recursively fill puzzle
                            puzzle[i][j] = 0  # backtrack
                    return  # trigger backtracking if there are no possibilities

        # we only get here if puzzle is solved
        solutions.append(puzzle.copy())

    solve(puzzle, solutions)

    # if there are no solutions, the puzzle is unsolvable
    if not solutions:
        return "UNSOLVABLE"

    # if we want 1 solution, don't return as a list
    if num_solutions == 1:
        assert len(solutions) == 1
        return solutions[0]

    # assert all solutions are unique
    flattened_tuple_solutions = map(lambda x: tuple(x.flatten()), solutions)
    unique_solutions = set(flattened_tuple_solutions)
    assert len(solutions) == len(unique_solutions), "Solutions found are not unique"

    return solutions
