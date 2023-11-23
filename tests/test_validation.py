import numpy as np
from src.puzzleloading.validation import validate_form


def test_validate_form():
    """
    Test validate_form
    """

    # test it works for valid puzzle with valid format
    valid_form1 = "tests/test_puzzles/valid.txt"
    puzzle1 = np.array(
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
    with open(valid_form1, "r") as file:
        text = file.read()
        valid, output = validate_form(text)
        assert valid
        assert np.array_equal(output, puzzle1)

    # test it works for puzzle with invalid format
    invalid_form1 = "tests/test_puzzles/invalid_form.txt"
    with open(invalid_form1, "r") as file:
        text = file.read()
        valid, output = validate_form(text)
        assert not valid
        assert output == "Too many digits on one or more rows."

    # test it works for invalid puzzle with valid format
    valid_form2 = "tests/test_puzzles/invalid_puzzle.txt"
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
    with open(valid_form2, "r") as file:
        text = file.read()
        valid, output = validate_form(text)
        assert valid
        assert np.array_equal(output, puzzle2)
