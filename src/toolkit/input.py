"""!@file io.py
@brief Module for handling inputs to the Sudoku solving program.

@details This module contains tools for loading and converting puzzles.

@author Created by William Knottenbelt
"""
import numpy as np
from .validation import validate_puzzle


def parse_sudoku_string(sudoku_str):
    """!
    @brief Parse Sudoku puzzle as a string into numpy array

    @details This function first validates that input string has a valid Sudoku
    puzzle format. If so, it returns a numpy array containing the puzzle, otherwise
    it returns the relevant error message explaining why the format is invalid.

    A valid Sudoku format is defined relatively flexibly:
    - A 9x9 grid of numbers (0-9)
    - Empty squares must be represented by 0's
    - Rows must be separated by new-lines
    - Digits (within rows) can be separated using any of the symbols: | - + ,
    - Rows can be separated using the same symbols.

    Note:
    The function does not check if the puzzle is solvable or if it adheres to
    Sudoku rules beyond formatting. It strictly checks the structural format.

    @param sudoku_str: str, The input string to be validated and parsed

    @return 9x9 numpy array representing puzzle if string represents valid Sudoku format,
    or error message if not.
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
        return f"Number of rows containing digits must be 9, but {n_rows} were given."

    for row in rows:
        # checking for non-digit characters left
        for char in row:
            if not char.isdigit():
                return f"Found unrecognised character '{char}'"

        # checking if there are 9 digits per row
        n_digits = len(row)
        if n_digits > 9:
            return "Too many digits on one or more rows."
        if n_digits < 9:
            return "Not enough digits on one or more rows."

    # convert to array
    puzzle = np.array([[int(char) for char in row] for row in rows])
    assert puzzle.shape == (9, 9)  # ensure shape is 9x9

    return puzzle


def load_puzzle(filepath, check_validity=True):
    """!@brief Function loads sudoku puzzles from text files to numpy arrays.

    @details
    The format for a sudoku puzzle just needs to be:
    - 9 digits in a row (can be separated by any of the following separators: | + - , or a space " ")
    - rows separated by new-lines
    - rows can also be separated by lines containing only the separators | + - , or spaces " "

    """

    # ensuring the file provided is a text file
    assert filepath[-4:] == ".txt"

    with open(filepath, "r") as file:
        text = file.read()

    # parse text in file
    # if valid format, output is 9x9 array containing puzzle
    output = parse_sudoku_string(text)
    if isinstance(output, np.ndarray):
        # output is array containing puzzle
        puzzle = output
    else:
        # output is error message
        print(f"File contains INVALID FORMAT: {output}")
        return None

    if check_validity:
        # validate that puzzle conforms to sudoku rules
        # if invalid, returns error message
        message = validate_puzzle(puzzle)
        if message != "Valid":
            print(f"Puzzle does not comply to sudoku rules: {message}")
            return None

    return puzzle
