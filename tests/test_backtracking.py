"""
This file does specific tests for the backtracking algorithm
"""

from src.toolkit.validation import validate_solution, validate_filled
from src.toolkit.io import load_puzzle

from src.engine.backtracking import backtracker
import numpy as np

# load puzzle with one solution
puzzle_one = load_puzzle("tests/test_puzzles/easy/easy_01.txt")

# load puzzle with 10 solutions
puzzle_many = load_puzzle("tests/test_puzzles/10_solutions.txt")


def test_single_solution():
    solution = backtracker(puzzle_one, num_solutions=1)
    assert validate_solution(puzzle_one, solution) == "Valid"

    solution = backtracker(puzzle_many, num_solutions=1)
    assert validate_solution(puzzle_many, solution) == "Valid"


def test_multiple_solutions():
    # suppose we ask for 3 solutions
    solutions = backtracker(puzzle_many, num_solutions=3)

    # assert we get list with 3 solutions
    assert isinstance(solutions, list) and len(solutions) == 3

    for solution in solutions:  # validate solutions
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
    Tests that backtracker discovers 3 puzzles are unsolvable
    """

    # path containing files
    path = "tests/test_puzzles/unsolvable/unsolvable_"

    for end in ["01.txt", "02.txt", "03.txt"]:
        puzzle = load_puzzle(path + end)
        assert backtracker(puzzle) == "UNSOLVABLE"
