"""!@file validation.py
@brief Module containing tools for validating puzzles

@author Created by William Knottenbelt
"""
import numpy as np


def validate_form(sudoku_str):
    """!
    @brief Validate the format of a Sudoku puzzle represented as a string.

    @details This function checks if the input string represents a valid Sudoku puzzle
    format. A valid Sudoku format is defined as a 9x9 grid of numbers (0-9),
    where rows are separated by newlines, and digits can be separated using
    symbols | - + ,
    If the input string is valid, we return an array containing the puzzle

    Note:
    The function does not check if the puzzle is solvable or if it adheres to
    Sudoku rules beyond formatting. It strictly checks the structural format.

    @param sudoku_str: str, The input string to be validated

    @return tuple containing two elements:
            - bool: True if the string has a valid format, False otherwise
            - If True, second element is array containing puzzle. If False, element is error message
    """
    if not isinstance(sudoku_str, str):
        raise ValueError("Parameter sudoku_str must be a string")

    # remove separators (special characters), spaces and empty lines
    sudoku_str = (
        sudoku_str.replace("|", "").replace("+", "").replace("-", "").replace(",", "")
    )
    sudoku_str = sudoku_str.replace(" ", "")
    sudoku_str = sudoku_str.replace("\n\n", "\n")

    # convert to list of rows
    rows = sudoku_str.split("\n")
    rows = [row for row in rows if row != ""]  # remove empty rows

    # check that there are now 9 rows,
    # each with exactly 9 characters
    # and the 9 characters are all digits [0-9]
    n_rows = len(rows)
    if n_rows != 9:
        return (
            False,
            f"Number of rows containing digits must be 9, but {n_rows} were given.",
        )

    for row in rows:
        # checking for non-digit characters left
        for char in row:
            if not char.isdigit():
                return (False, f"Found unrecognised character '{char}'")

        # checking if there are 9 digits per row
        n_digits = len(row)
        if n_digits > 9:
            return (False, "Too many digits on one or more rows.")
        if n_digits < 9:
            return (False, "Not enough digits on one or more rows.")

    # convert to array
    puzzle = np.array([[int(char) for char in row] for row in rows])
    assert puzzle.shape == (9, 9)  # ensure shape is 9x9

    return (True, puzzle)


def is_unique(arr):
    """!
    @brief Checks if all non-zero numbers in a 1D array are unique
    """
    arr = arr[arr > 0]  # Remove zeros
    return len(arr) == len(np.unique(arr))


def validate_puzzle(puzzle):
    """!
    @brief Check if a 9x9 numpy array is a valid Sudoku puzzle

    @details
    This function checks for correct dimensions, valid entries, and
    whether there are duplicate numbers in each row, column or 3x3
    block of the puzzle

    Note:
    The function does not check if the puzzle is solvable

    @param sudoku_arr: numpy.ndarray, A 9x9 NumPy array representing a Sudoku puzzle.

    @return str: "Valid" if the puzzle adheres to Sudoku rules, error message otherwise.
    """

    # check puzzle is numpy array
    assert isinstance(puzzle, np.ndarray)

    # check if the puzzle is 9x9
    if puzzle.shape != (9, 9):
        return "Invalid dimensions"

    # check if puzzle contains only integers from 0 to 9
    if not np.all(np.isin(puzzle, range(10))):
        return "Invalid entries"

    # check if puzzle is empty
    if np.array_equal(puzzle, np.zeros((9,9))):
        return "Puzzle is empty"

    # check each row, column, and 3x3 block
    for i in range(9):
        row = puzzle[i, :]
        col = puzzle[:, i]

        if not is_unique(row):
            return "Duplicate numbers in row(s)"

        if not is_unique(col):
            return "Duplicate numbers in column(s)"

        # vertical index of top left cell in block
        vert_i = 3 * (i // 3)

        # horizontal index of top left cell in block
        hor_i = 3 * (i % 3)

        block = puzzle[vert_i:vert_i + 3, hor_i:hor_i + 3]
        block = block.flatten()

        if not is_unique(block):
            return "Duplicate numbers in block(s)"

    return "Valid"
