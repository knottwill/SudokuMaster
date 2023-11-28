import numpy as np


def possibilities(puzzle, i, j):
    """!
    @brief Get possibile numbers for square (i,j)

    @details This is based only on standard sudoku rules: no
    duplicates in columns, rows or blocks. (It does not perform any
    advanced candidate elimination techniques)
    """
    row = puzzle[i]
    col = puzzle[:, j]

    # getting indices of the top left square in relevant block
    block_i = 3 * (i // 3)  # row index
    block_j = 3 * (j // 3)  # column index

    # getting block
    block = puzzle[block_i : block_i + 3, block_j : block_j + 3].flatten()

    # find all unique integers above 0 in row, col and block
    taken_numbers = set(set(row) | set(col) | set(block)) - set([0])

    # return which numbers are available to the square
    return set(range(1, 10)) - taken_numbers


def init_candidates(puzzle):
    """!
    @brief Initialises candidates grid from puzzle

    @details The candidate grid is a numpy array, where the
    item at index (i,j) is the set of possible candidates for the
    square at that index of the puzzle
    """
    candidates = np.empty((9, 9), dtype=object)
    for i in range(9):
        for j in range(9):
            if puzzle[i, j] == 0:  # at empty square, calculate possibilities
                candidates[i, j] = possibilities(puzzle, i, j)
            else:  # at a full square, the only possibility is that value
                candidates[i, j] = {puzzle[i, j]}
    return candidates


def filler(puzzle, candidates):
    """!
    @brief Fills puzzle using candidates grid

    @details If candidates grid has only one candidate for an empty
    square in the puzzle, we fill it in.
    """
    puzzle = puzzle.copy()
    for i in range(9):
        for j in range(9):
            cands = list(candidates[i, j])
            if puzzle[i, j] == 0:
                # if there is just one cadidate, fill it in
                if len(cands) == 1:
                    puzzle[i, j] = cands[0]
            else:
                # if a puzzle square is filled, then the candidate grid
                # must contain exactly that value
                assert (
                    len(cands) == 1 and cands[0] == puzzle[i, j]
                ), "Candidate grid at ({i},{j}) is not consistent with puzzle"
    return puzzle


def singles_filler(puzzle):
    """!
    @brief Fills in 'Naked Singles'

    This works via repeated application of init_candidates and filler
    """
    puzzle = puzzle.copy()

    # initially old puzzle must be different from puzzle
    # (except is puzzle is an empty board - then it doesn't matter)
    puzzle_old = np.zeros((9, 9), dtype=int)

    # we get candidates from the puzzle
    # then we fill the puzzle with the naked singles
    # and continue looping until puzzle stops changing
    while not np.array_equal(puzzle, puzzle_old):
        puzzle_old = puzzle
        candidates = init_candidates(puzzle)
        puzzle = filler(puzzle, candidates)

    return puzzle
