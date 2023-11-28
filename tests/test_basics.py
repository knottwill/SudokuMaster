import numpy as np
from src.engine.basics import init_candidates_grid


def test_init_candidates_grid():
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

    candidates = init_candidates_grid(puzzle)

    # check a few squares
    assert candidates[0, 0] == {2, 3, 5, 6, 8, 9}
    assert candidates[3, 3] == {1, 2, 4, 7}
    assert candidates[8, 0] == {5, 8, 9}
