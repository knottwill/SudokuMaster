"""!@file io.py
@brief Module for Output-related tools (relating to Sudoku puzzles).

@details This module contains tools for saving and printing puzzles
and candidate grids.

@author Created by William Knottenbelt
"""
import numpy as np
import os
from .validation import validate_puzzle


def puzzle_to_string(puzzle, check_validity=True):
    """!
    @brief Convert numpy array as sudoku puzzle to a string
    """

    # assert that the puzzle is a valid sudoku puzzle
    if check_validity:
        assert (
            validate_puzzle(puzzle) == "Valid"
        ), "The provided puzzle is not a valid sudoku puzzle"

    # convert the numpy array into the sudoku string format
    puzzle_str = ""
    for i, row in enumerate(puzzle):
        # add the row break at index 3 and 6
        if i in [3, 6]:
            puzzle_str += "---+---+---\n"

        row_str = "".join(str(num) for num in row)  # convert row to string
        puzzle_str += "|".join([row_str[i : i + 3] for i in [0, 3, 6]])  # add |
        puzzle_str += "\n"  # new line

    return puzzle_str


def save_puzzle(filepath, puzzle, check_validity=True):
    """!
    @brief Save a 9x9 numpy array as a sudoku puzzle to a given file.
    """
    # check that we are saving to a text file
    assert filepath.endswith(".txt"), "Filepath must end with .txt"

    # create the directory if it does not exist
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # get puzzle as string
    puzzle_str = puzzle_to_string(puzzle, check_validity)

    # Write the formatted string to the file
    with open(filepath, "w") as file:
        file.write(puzzle_str)


def print_puzzle(puzzle):
    """!
    @brief Prints numpy array as sudoku puzzle
    """
    puzzle_str = puzzle_to_string(puzzle)

    # add spaces after all digits
    puzzle_str = "".join(
        [char + " " if char.isdigit() else char for char in puzzle_str]
    )

    # add additional '-' so the printing looks correct
    puzzle_str = "".join([char + "-" if char == "-" else char for char in puzzle_str])

    print(puzzle_str)


def print_candidates(candidates):
    """!
    @brief prints candidates grid in a visually intuitive way
    """
    # output width of squares must be 10 (one more than max)
    # since the maxmimum candidates is '123456789'
    square_width = 10

    # array to store formatted candidates
    formatted_candidates = np.empty((9, 9), dtype=object)

    # convert each set of candidates to a string and pad it
    for i in range(9):
        for j in range(9):
            if candidates[i, j]:
                # conversion to string
                square_str = "".join(str(num) for num in sorted(candidates[i, j]))
                # padding to make all squares the same width
                formatted_candidates[i, j] = square_str.ljust(square_width)
            else:
                # if there are no candidates, square is empty
                formatted_candidates[i, j] = " " * square_width

    # print the formatted candidates with block separators
    for i, row in enumerate(formatted_candidates):
        row_str = ""
        for j, square in enumerate(row):
            row_str += square
            if (j + 1) % 3 == 0 and j < 8:
                row_str += "| "  # add separator after every 3 squares
        print(row_str)
        if (i + 1) % 3 == 0 and i < 8:
            print("-" * len(row_str))  # separator line after every 3 rows
