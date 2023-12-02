"""!@file generation.py
@brief Module containing functionality for generating Sudoku puzzles.

@details This module contains only a function to generate Sudoku puzzles
containing only 'Naked Singles'.

@author Created by W.D Knottenbelt
"""

from .validation import validate_solution, validate_puzzle
from ..engine.backtracking import backtracker
from ..engine.basics import singles_filler
import numpy as np
import random


def generate_singles():
    """!
    @brief Generates a Sudoku puzzle, solvable using only 'Naked Singles' technique.

    @details This function creates a puzzle by starting with a full board
    generated through backtracking. It then randomly proposes to empty certain squares
    and accepts these changes if the resulting puzzle can still be solved by filling
    in the naked singles. The process stops after 100 consecutive rejections
    of proposed changes.

    Reference: https://sudoku.com/sudoku-rules/obvious-singles/

    @return A 9x9 numpy array representing the generated puzzle.
    """

    # get random full board by filling empty board using backtracking
    empty = np.zeros((9, 9), dtype=int)
    puzzle = backtracker(empty)

    # ------------------------------------
    # We propose that a random square is made empty
    # We check if the resulting puzzle is solvable with the naked singles technique
    # If so, we accept the proposal, otherwise we reject
    # Carry on until 100 consecutive rejections
    # ------------------------------------
    n_subsequent_rejects = 0  # number of consecutive rejects
    n_accepts = 0  # number of empty squares created
    while n_subsequent_rejects < 100:
        # get indices of filled squares
        indices = np.nonzero(puzzle)
        paired_indices = list(zip(indices[0], indices[1]))

        # choose filled square at random
        idx = random.choice(paired_indices)

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
