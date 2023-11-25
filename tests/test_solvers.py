from src.toolkit.validation import validate_solution
from src.toolkit.io import load_puzzle

from src.engine.backtracking import backtracker


def test_backtracker():
    # test for valid puzzle
    filepath = "tests/test_puzzles/valid.txt"
    valid_puzzle = load_puzzle(filepath)

    solution = backtracker(valid_puzzle)  # solve puzzle

    assert validate_solution(valid_puzzle, solution) == "Valid"

    # test for invalid puzzle
    filepath = "tests/test_puzzles/unsolvable.txt"
    unsolvable_puzzle = load_puzzle(filepath, check_validity=False)
    solution = backtracker(unsolvable_puzzle)

    assert solution == "UNSOLVABLE"
