"""
Robust testing for the backtracking algorithm
"""

from src.toolkit.validation import validate_solution, validate_filled
from src.toolkit.input import load_puzzle

from src.engine.backtracking import backtracker
import numpy as np

# load puzzle with one solution
puzzle_one = load_puzzle("tests/test_puzzles/easy/easy_01.txt")

# load puzzle with 10 solutions
puzzle_many = load_puzzle("tests/test_puzzles/10_solutions.txt")


def test_single_solution():
    """
    Tests for finding single solutions using backtracking
    """
    solution = backtracker(puzzle_one, num_solutions=1)
    assert validate_solution(puzzle_one, solution) == "Valid"

    solution = backtracker(puzzle_many, num_solutions=1)
    assert validate_solution(puzzle_many, solution) == "Valid"


def test_multiple_solutions():
    """
    Tests for finding multiple solutions using backtracking
    """
    # we request for 3 solutions
    solutions = backtracker(puzzle_many, num_solutions=3)

    # assert we get list containing 3 solutions
    assert isinstance(solutions, list) and len(solutions) == 3

    # check each solution is valid
    for solution in solutions:
        assert validate_solution(puzzle_many, solution) == "Valid"

    # ---------------------------------------
    # getting multiple 'solutions' from empty board
    # ---------------------------------------
    empty_puzzle = np.zeros((9, 9)).astype(int)
    solutions = backtracker(empty_puzzle, num_solutions=3)

    # assert we recieved 3 solutions
    assert isinstance(solutions, list) and len(solutions) == 3

    # assert solutions are all different
    assert not np.all(solutions[0] == solutions[1])
    assert not np.all(solutions[0] == solutions[2])
    assert not np.all(solutions[1] == solutions[2])

    # assert they are valid full boards
    assert all(validate_filled(solutions[i]) == "Valid" for i in range(3))


def test_unsolvability():
    """
    Tests that backtracker identifies when puzzles are unsolvable
    """

    # path containing files
    path = "tests/test_puzzles/unsolvable/unsolvable_"

    for file in ["01.txt", "02.txt", "03.txt"]:
        puzzle = load_puzzle(path + file)
        assert backtracker(puzzle) == "UNSOLVABLE"
