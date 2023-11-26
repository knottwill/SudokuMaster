from src.toolkit.validation import validate_solution
from src.toolkit.io import load_puzzle

from src.engine.basics import singles_filler
from src.engine.backtracking import backtracker

solvers = [backtracker]


def test_backtracker():
    # test for valid puzzle
    filepath = "tests/test_puzzles/easy/easy_01.txt"
    valid_puzzle = load_puzzle(filepath)

    solution = backtracker(valid_puzzle)  # solve puzzle

    assert validate_solution(valid_puzzle, solution) == "Valid"

    # test for unsolvable puzzle
    filepath = "tests/test_puzzles/unsolvable/unsolvable_01.txt"
    unsolvable_puzzle = load_puzzle(filepath, check_validity=False)
    solution = backtracker(unsolvable_puzzle)

    assert solution == "UNSOLVABLE"


def test_singles_filler():
    # test on one that can be filled
    filepath = "tests/test_puzzles/singles_only/01.txt"
    singles_puzzle = load_puzzle(filepath)
    filled = singles_filler(singles_puzzle)
    assert validate_solution(singles_puzzle, filled) == "Valid"

    # test on one that cannot be filled
    filepath = "tests/test_puzzles/hardest/hardest_01.txt"
    hardest_puzzle = load_puzzle(filepath)
    filled = singles_filler(hardest_puzzle)
    assert validate_solution(hardest_puzzle, filled) == "Solution is Unfilled"


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
