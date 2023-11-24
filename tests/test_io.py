import numpy as np
from src.toolkit.io import load_puzzle, save_puzzle, puzzle_to_string
import pytest


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


def test_save_puzzle():
    """
    Test save_puzzle
    """

    # example valid puzzle
    real_path = "tests/test_puzzles/valid.txt"
    valid_puzzle = load_puzzle(real_path)

    # test for saving valid puzzle
    savepath = "puzzles/savetest.txt"
    save_puzzle(savepath, valid_puzzle)

    # read the file and check if the content is correct
    with open(savepath, "r") as saved_file, open(real_path, "r") as valid_file:
        saved_file.read() == valid_file.read()

    # test for invalid puzzle
    invalid_puzzle = np.zeros((9, 9))
    valid_savepath = "puzzles/never_exist.txt"
    with pytest.raises(AssertionError):
        save_puzzle(valid_savepath, invalid_puzzle)

    # test for invalid extension
    invalid_savepath = "puzzles/never_exist.py"
    with pytest.raises(AssertionError):
        save_puzzle(invalid_savepath, valid_puzzle)


def test_puzzle_to_string():
    # example valid puzzle
    filepath = "tests/test_puzzles/valid.txt"
    puzzle = load_puzzle(filepath)

    # read the file and check if the content is correct
    with open(filepath, "r") as file:
        content = file.read()

    assert puzzle_to_string(puzzle) == content
