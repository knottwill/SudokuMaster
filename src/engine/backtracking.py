import copy
import numpy as np
from src.engine.basics import init_candidates
from src.engine.elimination import all_elimination


def backtracker(puzzle, candidates=None, num_solutions=1):
    # check puzzle is numpy array with shape (9,9)
    assert isinstance(puzzle, np.ndarray) and puzzle.shape == (9, 9)

    puzzle = puzzle.copy()
    solutions = []

    def solve(puzzle, solutions, candidates):
        # break recursion when we have found enough solutions
        if len(solutions) >= num_solutions:
            return

        for i in range(9):  # iterate over rows
            for j in range(9):  # iterate over columns
                if puzzle[i][j] == 0:  # find an empty cell
                    numbers = list(candidates[i, j])
                    np.random.shuffle(numbers)  # introduce randomness

                    for n in numbers:
                        puzzle[i][j] = n  # fill square if number is a possibility

                        # create new candidates grid according to new puzzle
                        new_candidates = copy.deepcopy(candidates)
                        new_candidates[i, j] = {n}
                        new_candidates = all_elimination(new_candidates)

                        solve(
                            puzzle, solutions, new_candidates
                        )  # recursively fill puzzle

                        puzzle[i][j] = 0  # backtrack

                    return  # trigger backtracking if there are no possibilities

        # we only get here if puzzle is solved
        solutions.append(puzzle.copy())

    # initialise candidates grid if none is provided
    if candidates is None:
        candidates = init_candidates(puzzle)

    solve(puzzle, solutions, candidates)

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
