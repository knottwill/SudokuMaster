from src.toolkit.validation import validate_solution
from src.toolkit.io import load_puzzle

from src.engine.basics import singles_filler
from src.engine.backtracking import backtracker


def test_backtracker():
    # test for valid puzzle
    filepath = "tests/test_puzzles/easy/easy_01.txt"
    valid_puzzle = load_puzzle(filepath)

    solution = backtracker(valid_puzzle)  # solve puzzle

    assert validate_solution(valid_puzzle, solution) == "Valid"

    # test for unsolvable puzzle
    filepath = "tests/test_puzzles/unsolvable/unsolvable_01.txt"
    unsolvable_puzzle = load_puzzle(filepath, check_validity=False)
    solution = backtracker(unsolvable_puzzle)

    assert solution == "UNSOLVABLE"


def test_singles_filler():
    # test on one that can be filled
    filepath = "tests/test_puzzles/singles_only/01.txt"
    singles_puzzle = load_puzzle(filepath)
    filled = singles_filler(singles_puzzle)
    assert validate_solution(singles_puzzle, filled) == "Valid"

    # test on one that cannot be filled
    filepath = "tests/test_puzzles/hardest/hardest_01.txt"
    hardest_puzzle = load_puzzle(filepath)
    filled = singles_filler(hardest_puzzle)
    assert validate_solution(hardest_puzzle, filled) == "Solution is Unfilled"
