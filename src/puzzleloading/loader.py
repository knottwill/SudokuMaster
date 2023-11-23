"""!@file loader.py
@brief Module containing tools loading puzzles

@details This module contains tools for loading puzzles

@author Created by William Knottenbelt
"""

from src.puzzleloading.validation import validate_form, validate_puzzle


def load_puzzle(filepath):
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

    # Validate format of contents
    # if valid format, output is 9x9 array containing puzzle
    valid_format, output = validate_form(text)
    if valid_format:
        # output is array containing puzzle
        puzzle = output
    else:
        # output is error message
        print(f"File contains INVALID FORMAT: {output}")
        return 0

    # Validate that puzzle conforms to sudoku rules
    # if invalid, returns error message
    message = validate_puzzle(puzzle)
    if message != "Valid":
        print(f"Puzzle does not comply to sudoku rules: {message}")
        return 0

    return puzzle
