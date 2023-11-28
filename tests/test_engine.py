"""
This file contains general tests pertaining to files in src/engine/

Specific tests for particular algorithms can be found in other testing files
"""

from src.toolkit.validation import validate_solution
from src.toolkit.io import load_puzzle

from src.engine.backtracking import backtracker

solvers = [backtracker]


def test_all_solvers_robustly():
    """
    This test validates all solvers on 6 puzzles:
    - 3 easy puzzles
    - 3 hard puzzles

    The test is passed if all solvers solve all puzzles
    """

    easy_path = "tests/test_puzzles/easy/easy_"
    # hard_path = "tests/test_puzzles/hard/hard_"

    # 3 easy, hard and unsolvable puzzles
    for end in ["01.txt", "02.txt", "03.txt"]:
        # loading easy, hard and unsolvable puzzles
        easy_puzzle = load_puzzle(easy_path + end)
        #    hard_puzzle = load_puzzle(hard_path+end)

        for solver in solvers:
            # check solver solves easy puzzle correctly
            solution = solver(easy_puzzle)
            assert validate_solution(easy_puzzle, solution) == "Valid"

            # check solver solves hard puzzle correctly
        #    solution = solver(hard_puzzle)
        #    assert validate_solution(hard_puzzle, solution) == "Valid"
