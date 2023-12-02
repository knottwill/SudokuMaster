"""!@file basics.py
@brief Module for basic Sudoku solving utilities.

@details This module provides various functions to assist in solving Sudoku puzzles.
These functions include calculating the possible numbers for a specific square, initializing
candidate grids based on the puzzle, filling the puzzle using these candidates, and
checking if a puzzle is solvable. It also implements a method to fill in the 'Naked Singles'
of a Sudoku puzzle.

@author Created by W.D Knottenbelt
"""

import numpy as np


def possibilities(puzzle, i, j):
    """!
    @brief Get possible numbers for square in a Sudoku puzzle.

    @details Determines possible numbers for the square at index (i, j) in the Sudoku
    puzzle based on standard Sudoku rules: no duplicates in any row, column, or 3x3 block.
    Does not use advanced candidate elimination techniques.

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the puzzle.
    @param i (int) The row index of the square.
    @param j (int) The column index of the square.

    @return The set of possible numbers that can be placed in the square without
    causing immedate conflicts.
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
    @brief Initializes a candidates grid based on the current state of the Sudoku puzzle.

    @details Creates a 9x9 numpy array where the value at index (i, j) is the
    set of possible numbers that can occupy the square at index (i, j) in the
    puzzle, according to the "possibilities" function.

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the puzzle.

    @return A 9x9 numpy array representing the candidate grid.
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
    @brief Fills the puzzle using the provided candidates grid.

    @details Fills squares in the puzzle which have only one possible
    candidate according to the candidate grid ("candidates").

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the puzzle.
    @param candidates (numpy.ndarray) The candidate grid as a numpy array.

    @return The updated Sudoku puzzle as a numpy array.
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


def solvable(candidates):
    """!
    @brief Checks if the current candidates grid could correspond to a solvable puzzle.

    @details Checks whether any value in the candidates grid is an empty set.
    If so, there are no candidates for the corresponding square, hence the
    corresponding puzzle is unsolvable.
    Note: when this function returns True, it does not guarantee that the corresponding
    puzzle is solvable. It just means that currently every square has at least one
    candidate, but this does not necessarily make the puzzle solvable.

    @param candidates (numpy.ndarray) The candidate grid as a numpy array.

    @return True if the puzzle is solvable, False otherwise.
    """
    for i in range(9):
        for j in range(9):
            # if any square has no candidates, the puzzle is unsolvable
            if not candidates[i, j]:
                return False
    # returns true if all squares have one or more candidates
    # (does not necessarily mean the puzzle is actually solvable)
    return True


def singles_filler(puzzle):
    """!
    @brief Fills in 'Naked Singles' (AKA Obvious Singles) in the puzzle.

    @details A 'Naked Single' is a square in the puzzle that has only one candidate.
    The function works by initializing the candidate grid from the current state of
    the puzzle, then filling the puzzle using the grid, and repeating this process
    until the puzzle stops changing.

    Reference: https://sudoku.com/sudoku-rules/obvious-singles/

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the puzzle.

    @return The updated puzzle as a numpy array
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
