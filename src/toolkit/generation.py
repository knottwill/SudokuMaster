from .validation import validate_solution, validate_puzzle
from ..engine.backtracking import backtracker
from ..engine.basics import singles_filler
import numpy as np
import random


def generate_singles():
    """!
    @brief Randomly generate a puzzle that contains only naked singles and hidden singles
    """

    # initialise empty sudoku board
    empty = np.zeros((9, 9)).astype(int)

    # get random full board by filling it in with backtracking
    puzzle = backtracker(empty)

    # ------------------------------------
    # We propose that a square becomes empty
    # We check if the resulting puzzle contains only naked singles
    # If so, we accept the proposal, otherwise we reject
    # ------------------------------------
    n_subsequent_rejects = 0  # number of rejects in a row
    n_accepts = 0  # number of empty squares created
    while n_subsequent_rejects < 100:  # if we fail 100 times in a row, we stop trying
        # get indices of filled squares
        indices = np.nonzero(puzzle)
        paired_indices = list(zip(indices[0], indices[1]))

        idx = random.choice(paired_indices)  # randomly choose filled square

        # attempt to make square empty
        puzzle_copy = puzzle.copy()
        puzzle_copy[idx] = 0

        # fill in singles and check if this yields solution
        solution = singles_filler(puzzle_copy)
        message = validate_solution(puzzle_copy, solution)

        # either the solution should be valid or it should contain empty squares
        assert message == "Valid" or message == "Solution is Unfilled"

        # if the singles_filler found solution then we accept the empty square
        if message == "Valid":
            puzzle[idx] = 0  # accept
            n_subsequent_rejects = 0
            n_accepts += 1
        else:  # reject
            n_subsequent_rejects += 1

    # the number of empty squares in the final puzzle
    # should be the same as the number of times we accepted an empty square
    assert np.sum(puzzle == 0) == n_accepts

    assert validate_puzzle(puzzle) == "Valid"  # assert puzzle is valid

    return puzzle
