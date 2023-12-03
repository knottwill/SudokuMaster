"""
Robust testing for toolkit/input.py and toolkit/output.py
"""

import numpy as np
import os
from src.toolkit.input import load_puzzle, parse_sudoku_string
from src.toolkit.output import save_puzzle, puzzle_to_string
import pytest


def test_parse_sudoku_string():
    """
    Test parse_sudoku_string
    """

    # test on valid puzzle with valid format
    filepath1 = "tests/test_puzzles/easy/easy_01.txt"
    puzzle1 = np.array(
        [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0],
        ]
    )
    with open(filepath1, "r") as file:
        text = file.read()
        output = parse_sudoku_string(text)
        assert isinstance(output, np.ndarray)
        assert np.array_equal(output, puzzle1)

    # test on invalid puzzle with valid format
    filepath2 = "tests/test_puzzles/invalid/invalid_puzzle.txt"
    puzzle2 = np.array(
        [
            [0, 0, 0, 0, 0, 7, 5, 0, 0],  # notice 5 is used twice in the 7th column
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
    with open(filepath2, "r") as file:
        text = file.read()
        output = parse_sudoku_string(text)
        assert isinstance(output, np.ndarray)
        assert np.array_equal(output, puzzle2)

    # test on puzzle with invalid format
    filepath3 = "tests/test_puzzles/invalid/invalid_form.txt"
    with open(filepath3, "r") as file:
        text = file.read()
        output = parse_sudoku_string(text)
        assert isinstance(output, str)
        assert output == "Too many digits on one or more rows."


def test_load_puzzle():
    """
    Test load_puzzle
    """
    valid_puzzle = np.array(
        [
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0],
        ]
    )

    # valid puzzle
    loaded_item = load_puzzle("tests/test_puzzles/easy/easy_01.txt")
    assert np.array_equal(loaded_item, valid_puzzle)

    # puzzle with invalid format
    loaded_item = load_puzzle("tests/test_puzzles/invalid/invalid_form.txt")
    assert loaded_item is None

    # invalid puzzle (does not conform to sudoku rules)
    loaded_item = load_puzzle("tests/test_puzzles/invalid/invalid_puzzle.txt")
    assert loaded_item is None


def test_puzzle_to_string():
    """
    Test puzzle_to_string
    """
    # example valid puzzle
    filepath = "tests/test_puzzles/easy/easy_01.txt"
    puzzle = load_puzzle(filepath)

    # read the file and check if the content is correct
    with open(filepath, "r") as file:
        content = file.read()

    assert puzzle_to_string(puzzle) == content


def test_save_puzzle():
    """
    Test save_puzzle
    """

    # -----------------
    # Test on valid puzzle
    # ------------------

    # load valid puzzle
    filepath = "tests/test_puzzles/easy/easy_01.txt"
    valid_puzzle = load_puzzle(filepath)

    # save puzzle to different location
    savepath = "tests/test_puzzles/savetest.txt"
    save_puzzle(savepath, valid_puzzle)  # save puzzle

    # read both files and check that the saved content is correct
    with open(savepath, "r") as saved_file, open(filepath, "r") as valid_file:
        saved_file.read() == valid_file.read()

    # delete saved puzzle
    os.remove(savepath)

    # -----------------
    # Test for invalid extension
    # ------------------

    # should raise an error when trying to save a puzzle in a .py file
    invalid_savepath = "tests/test_puzzles/never_exist.py"
    with pytest.raises(AssertionError):
        save_puzzle(invalid_savepath, valid_puzzle)

    # ---------------
    # Test on invalid puzzle
    # ----------------

    filepath = "tests/test_puzzles/invalid/invalid_puzzle.txt"
    invalid_puzzle = load_puzzle(filepath, check_validity=False)
    valid_savepath = "tests/test_puzzles/never_exist.txt"

    # should raise an error when attempting to save an invalid puzzle
    with pytest.raises(AssertionError):
        save_puzzle(valid_savepath, invalid_puzzle)
