import numpy as np

filepath = 'puzzles/valid.txt'

def validate_form(sudoku_str):
    """
    Validate the format of a Sudoku puzzle represented as a string.

    This function checks if the input string represents a valid Sudoku puzzle
    format. A valid Sudoku format is defined as a 9x9 grid of numbers (0-9),
    separated, according to our convention, using symbols | - + and newlines.

    Note:
    The function does not check if the puzzle is solvable or if it adheres to
    Sudoku rules beyond formatting. It strictly checks the structural format.

    Parameters
    -----------
    sudoku_str: str
        the input string to be validated

    Returns
    -----------
    bool
        True if the string has the valid format, False otherwise
    """

    if not isinstance(sudoku_str, str):
        raise ValueError('')
    
def validate_puzzle(sudoku_arr):
    """
    Check if a 9x9 NumPy array adheres to Sudoku rules

    The function verifies that each number 1-9 appears no more than once in 
    each row, column, and 3x3 subgrid of the puzzle.

    Note:
    The function does not check if the puzzle is solvable

    Parameters
    -----------
    sudoku_arr: numpy.ndarray
        A 9x9 NumPy array representing a Sudoku puzzle.

    Returns
    -----------
    bool
        True if the puzzle adheres to Sudoku rules, False otherwise.
    """

    # check its a numpy array

    # check its shape is (9,9)
