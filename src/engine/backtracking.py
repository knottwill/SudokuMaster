"""!@file backtracking.py
@brief Module containing functionality for solving Sudoku using backtracking

@author Created by W.D Knottenbelt
"""

import copy
import numpy as np
from .basics import init_candidates
from .elimination import all_elimination


def solve(puzzle, solutions, candidates, num_solutions=1):
    """!
    @brief Recursive function to solve a Sudoku puzzle using backtracking.

    @details This function operates by filling empty squares in the puzzle with the possible
    candidates for that square, as determined by the candidates grid, and then recursively calling
    itself to proceed to the next square. Once a square is reached that has no candidates,
    the function backtracks and empties the last-filled square, and tries the next candidate.
    When a solution is found, it is appended to the solutions list, and continues backtracking
    to find additional solutions. When the desired number of solutions is found, the condition is
    triggered to break out of all recursive calls.

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the Sudoku puzzle.
    @param solutions (list) A list to store the solutions found.
    @param candidates (numpy.ndarray) A 9x9 numpy array containing the possible candidate numbers for each square.
    @param num_solutions (int, optional) The number of solutions to find (default is 1).

    @return None. The function modifies the solutions list in place.
    """
    # break recursion when we have found enough solutions
    if len(solutions) >= num_solutions:
        return

    for i in range(9):  # iterate over rows
        for j in range(9):  # iterate over columns
            if puzzle[i, j] == 0:  # find an empty square
                numbers = list(candidates[i, j])
                np.random.shuffle(numbers)  # introduce randomness

                for n in numbers:
                    puzzle[i, j] = n  # fill square if number is a possibility

                    # create new candidates grid according to new puzzle
                    new_candidates = copy.deepcopy(candidates)
                    new_candidates[i, j] = {n}
                    new_candidates = all_elimination(new_candidates)

                    solve(
                        puzzle, solutions, new_candidates, num_solutions
                    )  # recursively fill puzzle

                    puzzle[i, j] = 0  # backtrack

                return  # trigger backtracking if there are no possibilities

    # we only get here if puzzle is solved
    solutions.append(puzzle.copy())


def backtracker(puzzle, candidates=None, num_solutions=1):
    """!
    @brief Function to run the backtracking process for solving Sudoku puzzles.

    @details Initiates the backtracking algorithm. Sets up necessary data structures and checks,
    and calls the recursive 'solve' function. Handles scenarios where no solutions are found
    and ensures uniqueness of solutions.

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the Sudoku puzzle.
    @param candidates (numpy.ndarray, optional) Precomputed candidate numbers for each square. Initialized if None.
    @param num_solutions (int, optional) The number of solutions to find (default is 1).

    @return A single solution array if one solution is requested, a list of solutions if
    multiple solutions are requested, or the string "UNSOLVABLE" if no solutions are found.
    """
    # check puzzle is numpy array with shape (9,9)
    assert isinstance(puzzle, np.ndarray) and puzzle.shape == (9, 9)

    puzzle = puzzle.copy()
    solutions = []

    # initialise candidates grid if none is provided
    if candidates is None:
        candidates = init_candidates(puzzle)

    # type-check candidates grid
    assert isinstance(candidates, np.ndarray) and candidates.dtype == object

    # find solutions
    solve(puzzle, solutions, candidates, num_solutions)

    # if there are no solutions, the puzzle is unsolvable
    if not solutions:
        return "UNSOLVABLE"

    # if 1 solution is specified, return just the array (not in a list)
    if num_solutions == 1:
        assert len(solutions) == 1
        return solutions[0]

    # assert all solutions are unique
    flattened_tuple_solutions = map(lambda x: tuple(x.flatten()), solutions)
    unique_solutions = set(flattened_tuple_solutions)
    assert len(solutions) == len(unique_solutions), "Solutions found are not unique"

    return solutions
