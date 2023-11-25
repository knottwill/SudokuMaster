"""!@file validation.py
@brief Module containing tools for validating puzzles

@author Created by William Knottenbelt
"""
import numpy as np


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
    if np.array_equal(puzzle, np.zeros((9, 9))):
        return "Puzzle is empty"

    # check each row, column, and 3x3 block
    for n in range(9):
        row = puzzle[n, :]  # n-th row
        col = puzzle[:, n]  # n-th column

        # indices of the top left square in n-th block
        block_i = 3 * (n // 3)  # row index
        block_j = 3 * (n % 3)  # column index

        block = puzzle[block_i : block_i + 3, block_j : block_j + 3]
        block = block.flatten()

        if not is_unique(row):
            return "Duplicate numbers in row(s)"

        if not is_unique(col):
            return "Duplicate numbers in column(s)"

        if not is_unique(block):
            return "Duplicate numbers in block(s)"

    return "Valid"
