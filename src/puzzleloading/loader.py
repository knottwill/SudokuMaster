"""!@file loader.py
@brief Module containing tools loading puzzles

@details This module contains tools for loading puzzles

@author Created by William Knottenbelt
"""

import numpy as np


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

    # remove separators (special characters), spaces and empty lines
    text = text.replace("|", "").replace("+", "").replace("-", "").replace(",", "")
    text = text.replace(" ", "")
    text = text.replace("\n\n", "\n")

    # convert to list of rows
    rows = text.split("\n")
    rows = [row for row in rows if row != ""]  # remove empty rows

    # ------------
    # Add functionality to validate puzzle
    # ------------

    # convert to array
    puzzle = np.array([[int(char) for char in row] for row in rows])

    return puzzle
