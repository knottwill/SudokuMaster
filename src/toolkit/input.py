"""!@file output.py
@brief Module for handling inputs to the Sudoku solving program.

@details This module contains tools for loading and parsing puzzles.

@author Created by William Knottenbelt
"""
import numpy as np
from .validation import validate_puzzle


def parse_sudoku_string(sudoku_str):
    """!
    @brief Parse Sudoku puzzle as a string into numpy array

    @details This function first validates that the input string conforms to the
    specific formatting criteria of a Sudoku puzzle (detailed below).
    If so, it returns a numpy array containing the puzzle, otherwise
    it returns the relevant error message explaining why the format is invalid.

    A valid Sudoku format is defined relatively flexibly:
    - A 9x9 grid of numbers (0-9)
    - Empty squares must be represented by 0's
    - Rows must be separated by new-lines
    - Digits (within rows) can be separated using any of the symbols: | - + ,
    - Digits can also be separated using spaces
    - Rows can be separated using the same symbols or empty lines
    - Row-separating lines can never contain digits

    Note:
    The function does not check if the puzzle is solvable or if it adheres to
    Sudoku rules beyond formatting. It strictly checks the structural format.

    @param sudoku_str (str) The input string to be validated and parsed

    @return 9x9 numpy array representing puzzle if string represents valid Sudoku format,
    or error message if not.
    """
    assert isinstance(sudoku_str, str), "Parameter sudoku_str must be a string"

    # remove separators (special characters), spaces and empty lines
    sudoku_str = (
        sudoku_str.replace("|", "").replace("+", "").replace("-", "").replace(",", "")
    )
    sudoku_str = sudoku_str.replace(" ", "")
    sudoku_str = sudoku_str.replace("\n\n", "\n")

    # convert to list of rows
    rows = sudoku_str.split("\n")
    rows = [row for row in rows if row != ""]  # remove empty rows

    # ------------------------
    # check that there are now 9 rows,
    # each with exactly 9 characters
    # and the 9 characters are all digits [0-9]
    # -------------------------

    n_rows = len(rows)
    if n_rows != 9:
        return f"Number of rows containing digits must be 9, but {n_rows} were given."

    for row in rows:
        # checking for non-digit characters leftover
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
    """!
    @brief Load a Sudoku puzzle from a text file into a numpy array.

    @details The function reads a Sudoku puzzle from a specified text file and
    converts it into a 9x9 numpy array. The puzzle in the text file should
    adhere to specific formatting criteria: each row must contain 9 digits,
    separated by '|', '+', '-', ',', or a space ' '. Rows are separated by
    newline characters, and they may also be separated by lines containing
    only the specified separators. The function has an option to validate the
    Sudoku puzzle against standard Sudoku rules. If the puzzle format is invalid
    or does not conform to Sudoku rules (when validation is enabled), the function
    returns 'None'.

    @param filepath (str) The filepath of the Sudoku puzzle text file.
    @param check_validity (bool, optional) Flag to indicate whether to validate
    the Sudoku puzzle against standard Sudoku rules. Defaults to True.

    @return A 9x9 numpy array representing the Sudoku puzzle if the file
    format and puzzle are valid; otherwise, returns 'None'.
    """
    # ensuring the file provided is a text file
    assert filepath[-4:] == ".txt", "File must have extension .txt"

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
        message = validate_puzzle(puzzle)
        if message != "Valid":
            print(f"Puzzle does not comply to sudoku rules: {message}")
            return None

    return puzzle
