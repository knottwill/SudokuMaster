import numpy as np
from src.toolkit.io import load_puzzle
from src.toolkit.validation import validate_solution
from src.engine.basics import init_candidates, filler, singles_filler


def test_init_candidates():
    # test for empty puzzle
    puzzle = np.zeros((9, 9), dtype=int)
    candidates = init_candidates(puzzle)
    for i in range(9):
        for j in range(9):
            assert candidates[i, j] == set(
                [1, 2, 3, 4, 5, 6, 7, 8, 9]
            ), "All numbers must be candidates for all squares in an empty puzzle"

    # test for an actual puzzle
    puzzle = np.array(
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

    candidates = init_candidates(puzzle)

    # check a few squares
    assert candidates[0, 0] == {2, 3, 5, 6, 8, 9}
    assert candidates[3, 3] == {1, 2, 4, 7}
    assert candidates[8, 0] == {5, 8, 9}


def test_filler():
    """
    Test filler function.
    """
    puzzle = np.array(
        [
            [0, 2, 3, 4, 5, 6, 7, 8, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    candidates = init_candidates(puzzle)
    puzzle = filler(puzzle, candidates)

    assert puzzle[0, 0] == 1


def test_singles_filler():
    # test on all files containing naked singles only
    dirpath = "tests/test_puzzles/singles_only/"
    for file in ["01.txt", "02.txt", "03.txt"]:
        filepath = dirpath + file
        puzzle = load_puzzle(filepath)
        filled = singles_filler(puzzle)
        assert validate_solution(puzzle, filled) == "Valid"

    # test on one that cannot be filled
    filepath = "tests/test_puzzles/hardest/hardest_01.txt"
    hardest_puzzle = load_puzzle(filepath)
    filled = singles_filler(hardest_puzzle)
    assert validate_solution(hardest_puzzle, filled) == "Solution is Unfilled"
