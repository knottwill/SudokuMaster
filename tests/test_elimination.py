import numpy as np
from src.engine.basics import init_candidates
from src.engine.elimination import naked_singles_elimination


def test_naked_singles_elimination():
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
