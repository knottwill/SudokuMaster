"""!@file input.py
@brief Module for handling outputs of Sudoku solving program.

@details This module contains tools for saving and printing puzzles
and candidate grids.

@author Created by William Knottenbelt
"""
import numpy as np
import os
from .validation import validate_puzzle


def puzzle_to_string(puzzle, check_validity=True):
    """!
    @brief Convert a Sudoku puzzle from a numpy array to a string representation.

    @details This function takes a 9x9 numpy array representing a Sudoku puzzle
    and converts it into a string, formatted according to our specific criteria:
    - Rows (each containing 9 digits) are separated by newlines
    - Separator '|' added after every third digit in a row
    - Row separator '---+---+---' added after every third row

    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the Sudoku puzzle.
    @param check_validity (bool, optional) Flag to indicate whether the puzzle
    should be validated before conversion. Defaults to True.

    @return A string representation of the Sudoku puzzle, formatted with row and digit separators.

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
    @brief Save a Sudoku puzzle as a numpy array to a given file.

    @details This function saves a Sudoku puzzle into a text file at the
    filepath provided. The necessary directories in the filepath are
    created if they do not exist.

    @param filepath (str) The file path where the Sudoku puzzle will be saved. Must end with '.txt'.
    @param puzzle (numpy.ndarray) A 9x9 numpy array representing the Sudoku puzzle.
    @param check_validity (bool, optional) Flag to indicate whether the puzzle should be
    validated before saving. Defaults to True.
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
    @brief Prints numpy array representing a Sudoku puzzle in a visually intuitive way.

    @details The function prints the puzzle in the format given by puzzle_to_string,
    except with spaces added after each digit for better readability.

    @param puzzle (numpy.ndarray): A 9x9 numpy array representing the Sudoku puzzle.
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
    @brief Prints the candidates grid for a Sudoku puzzle in a visually intuitive way.

    @details This function takes a 9x9 grid of candidate sets for a Sudoku puzzle
    and prints it in a formatted, readable manner. The function converts the candidate
    sets to strings, pads them so that each square has the same length, and prints the
    grid with separators.

    @param candidates (numpy.ndarray) The candidates grid as a numpy array.
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
