import numpy as np
from src.toolkit.input import load_puzzle
from src.toolkit.validation import validate_solution
from src.engine.basics import init_candidates, filler, solvable
from src.engine.elimination import (
    naked_singles_elimination,
    hidden_singles_elimination,
    obvious_pairs_elimination,
    pointing_elimination,
    all_elimination,
)


def test_naked_singles():
    # candidates for empty array (all numbers for all squares)
    puzzle = np.zeros((9, 9), dtype=int)
    candidates = init_candidates(puzzle)

    # manually insert naked single
    candidates[0, 0] = {3}

    candidates = naked_singles_elimination(candidates)

    # union of all candidates in the rest of the row and column
    rest_of_row = set().union(*candidates[0, 1:])
    rest_of_col = set().union(*candidates[1:, 0])

    # union of all candidates in the rest of the block
    rest_of_block = set().union(
        *candidates[1:2, 0],  # two squares below (0,0)
        *candidates[0, 1:2],  # two squares right of (0,0)
        *candidates[1:2, 1:2].flatten()  # 4 squares in rest of block
    )

    # assert that 3 has been eliminated from the rest of the row, column or block
    assert {3}.isdisjoint(rest_of_row), "Single not eliminated from rest of row"
    assert {3}.isdisjoint(rest_of_col), "Single not eliminated from rest of column"
    assert {3}.isdisjoint(rest_of_block), "Single not eliminated from rest of block"


def test_hidden_singles():
    # candidates for empty array (all numbers for all squares)
    puzzle = np.zeros((9, 9), dtype=int)
    candidates = init_candidates(puzzle)

    # manually insert hidden single to (0,0) by
    # removing 3's from it's column
    for i in range(1, 9):
        candidates[i, 0].discard(3)

    # manually insert hidden single to (2,8) by
    # removing 4's from its row
    for j in range(0, 8):
        candidates[2, j].discard(4)

    # insert hidden single to (8,8) by
    # removing 6's from its block
    idx = (8, 8)
    block_i = 3 * (idx[0] // 3)
    block_j = 3 * (idx[1] // 3)
    for i in range(block_i, block_i + 3):
        for j in range(block_j, block_j + 3):
            if (i, j) != idx:
                candidates[i, j].discard(6)

    # perform hidden singles elimination
    candidates = hidden_singles_elimination(candidates)

    assert candidates[0, 0] == {3}, "Failed to find hidden single in column"
    assert candidates[2, 8] == {4}, "Failed to find hidden single in row"
    assert candidates[8, 8] == {6}, "Failed to find hidden single in block"


def test_obvious_pairs():
    # candidates for empty array (all numbers for all squares)
    puzzle = np.zeros((9, 9), dtype=int)
    candidates = init_candidates(puzzle)

    # manually insert obvious pair (in first block & row)
    candidates[0, 0] = {3, 4}
    candidates[0, 1] = {3, 4}

    # run elimination
    candidates = obvious_pairs_elimination(candidates)

    # union of all candidates in the rest of the row
    rest_of_row = set().union(*candidates[0, 2:])

    # union of all candidates in the rest of the block
    rest_of_block = set().union(
        *candidates[1:2, 0],  # two squares below (0,0)
        candidates[0, 2],  # square to the right of (0,1)
        *candidates[1:2, 1:2].flatten()  # 4 squares in rest of block
    )

    # assert that 3 has been eliminated from the rest of the row, column or block
    assert {3, 4}.isdisjoint(rest_of_row), "Pair not eliminated from rest of row"
    assert {3, 4}.isdisjoint(rest_of_block), "Pair not eliminated from rest of block"


def test_pointing():
    # candidates for empty array (all numbers for all squares)
    puzzle = np.zeros((9, 9), dtype=int)
    candidates = init_candidates(puzzle)

    # manually insert pointing triple along first row
    # by discarding 3's from the other rows in the first block
    for i in range(1, 3):
        for j in range(3):
            candidates[i, j].discard(3)

    # insert pointing triple along last column
    # by discarding 4's from other columns in bottom right block
    for i in range(6, 9):
        for j in range(6, 8):
            candidates[i, j].discard(4)

    # run elimination
    candidates = pointing_elimination(candidates)

    # union of all candidates in the rest of the row
    rest_of_row = set().union(*candidates[0, 3:])

    # union of all candidates in the rest of the row
    rest_of_col = set().union(*candidates[:6, 8])

    # assert that 3 has been eliminated from the rest of the row, column or block
    assert {3}.isdisjoint(rest_of_row), "Number not eliminated from rest of row"
    assert {4}.isdisjoint(rest_of_col), "Number not eliminated from rest of column"


def test_all_elimination():
    # all 3 easy puzzles can be solved using only elimination techniques
    path = "tests/test_puzzles/easy/easy_"

    for file in ["01.txt", "02.txt", "03.txt"]:
        filepath = path + file
        puzzle = load_puzzle(filepath)
        candidates = init_candidates(puzzle)

        # run elimination
        candidates = all_elimination(candidates)

        # fill puzzle
        solution = filler(puzzle, candidates)

        # asserting that puzzle has not been modified
        assert not np.array_equal(puzzle, solution)

        # asserting solution has been found
        assert validate_solution(puzzle, solution) == "Valid"

    # test on unsolvable puzzle
    filepath = "tests/test_puzzles/unsolvable/unsolvable_01.txt"
    puzzle = load_puzzle(filepath)
    candidates = init_candidates(puzzle)
    candidates = all_elimination(candidates)
    assert not solvable(candidates)
