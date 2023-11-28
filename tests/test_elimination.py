import numpy as np
from src.engine.basics import init_candidates
from src.engine.elimination import (
    naked_singles_elimination,
    hidden_singles_elimination,
    obvious_pairs_elimination,
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
