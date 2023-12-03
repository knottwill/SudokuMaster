from src.toolkit.generation import generate_singles
from src.toolkit.validation import validate_solution
from src.engine.basics import singles_filler


def test_generate_singles():
    """
    Test generate_singles

    Simple test that ensures this function generates a puzzle
    which is solvable purely by repeatedly filling in naked singles
    """

    puzzle = generate_singles()
    solution = singles_filler(puzzle)

    assert (
        validate_solution(puzzle, solution) == "Valid"
    ), "Solution not found by 'singles_filler'"
