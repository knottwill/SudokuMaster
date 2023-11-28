import numpy as np
from src.engine.basics import init_candidates
from src.engine.elimination import naked_singles_elimination


def test_naked_singles_elimination():
    puzzle = np.zeros((9, 9), dtype=int)
    candidates = init_candidates(puzzle)
    # Manually set naked single
    candidates[0, 0] = {3}

    candidates = naked_singles_elimination(candidates)

    # assert 3 not in first row, column or block
    rest_of_row = set().union(*candidates[0, 1:])
    rest_of_col = set().union(*candidates[1:, 0])
    rest_of_block = set().union(*candidates[0:2, 0:2].flatten())

    assert {3}.isdisjoint(rest_of_row), "Single not eliminated from rest of row"
    assert {3}.isdisjoint(rest_of_col), "Single not eliminated from rest of column"
    assert {3}.isdisjoint(rest_of_block), "Single not eliminated from rest of block"
