from src.toolkit.validation import validate_solution, validate_filled
from src.toolkit.io import load_puzzle

from src.engine.backtracking import backtracker
import numpy as np


def test_backtracker():
    # test for valid puzzle
    filepath = "tests/test_puzzles/easy/easy_01.txt"
    valid_puzzle = load_puzzle(filepath)

    solution = backtracker(valid_puzzle)  # solve puzzle

    assert validate_solution(valid_puzzle, solution) == "Valid"

    # test for invalid puzzle
    filepath = "tests/test_puzzles/unsolvable/unsolvable_01.txt"
    unsolvable_puzzle = load_puzzle(filepath, check_validity=False)
    solution = backtracker(unsolvable_puzzle)

    assert solution == "UNSOLVABLE"


def test_multiple_solution_backtracking():
    # test for puzzle with exactly 1 solution
    filepath = "tests/test_puzzles/easy/easy_01.txt"
    valid_puzzle = load_puzzle(filepath)

    solution = backtracker(valid_puzzle, num_solutions=1)
    assert isinstance(solution, np.ndarray)
    assert validate_solution(valid_puzzle, solution) == "Valid"

    # same but we ask for multiple solutions
    solutions = backtracker(valid_puzzle, num_solutions=3)
    assert isinstance(solutions, list) and len(solutions) == 1
    assert validate_solution(valid_puzzle, solutions[0])

    # ---------------------------------------
    # getting multiple 'solutions' from empty board
    # ---------------------------------------
    empty_puzzle = np.zeros((9, 9)).astype(int)
    solutions = backtracker(empty_puzzle, num_solutions=3)

    # assert we recieved 3 solutions
    assert isinstance(solutions, list) and len(solutions) == 3

    # assert solutions are all different
    assert not all(solutions[0] == solutions[1])
    assert not all(solutions[0] == solutions[2])
    assert not all(solutions[1] == solutions[2])

    # assert they are valid full boards
    assert all(validate_filled(solutions[i]) == "Valid" for i in range(3))
