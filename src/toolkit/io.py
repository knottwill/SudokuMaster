"""!@file io.py
@brief Module for Input/Output of Sudoku puzzles.

@details This module contains tools for loading, saving, converting and
printing puzzles. It also contains a function to print candidate grids.

@author Created by William Knottenbelt
"""
import numpy as np
import os
from .validation import validate_puzzle


def parse_sudoku_string(sudoku_str):
    """!
    @brief Validate the format of a Sudoku puzzle as a string, and parse into numpy array.

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

    # validate format of contents
    # if valid format, output is 9x9 array containing puzzle
    valid_format, output = parse_sudoku_string(text)
    if valid_format:
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
