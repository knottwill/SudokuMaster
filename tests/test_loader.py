import numpy as np
from src.puzzleloading.loader import load_puzzle


def test_load_puzzle():
    """
    Test load_puzzle
    """
    valid_puzzle = np.array(
        [
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 5, 0, 4],
            [0, 0, 0, 0, 5, 0, 1, 6, 9],
            [0, 8, 0, 0, 0, 0, 3, 0, 5],
            [0, 7, 5, 0, 0, 0, 2, 9, 0],
            [4, 0, 6, 0, 0, 0, 0, 8, 0],
            [7, 6, 2, 0, 8, 0, 0, 0, 0],
            [1, 0, 3, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 0],
        ]
    )

    # valid puzzle
    loaded_item = load_puzzle("tests/test_puzzles/valid.txt")
    assert np.array_equal(loaded_item, valid_puzzle)

    # puzzle with invalid format
    loaded_item = load_puzzle("tests/test_puzzles/invalid_form.txt")
    assert loaded_item == 0

    # invalid puzzle (does not conform to sudoku rules)
    loaded_item = load_puzzle("tests/test_puzzles/invalid_puzzle.txt")
    assert loaded_item == 0
