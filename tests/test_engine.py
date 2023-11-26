from src.toolkit.validation import validate_solution
from src.toolkit.io import load_puzzle

from src.engine.basics import singles_filler


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
