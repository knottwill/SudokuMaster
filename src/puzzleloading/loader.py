"""!@file loader.py
@brief Module containing tools loading puzzles

@details This module contains tools for loading and saving puzzles

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


def puzzle_to_string(puzzle):
    """!
    @brief Convert numpy array as sudoku puzzle to a string
    """

    # assert that the puzzle is a valid sudoku puzzle
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
        puzzle_str += "|".join([row_str[i:i + 3] for i in [0, 3, 6]])  # add |
        puzzle_str += "\n"  # new line

    return puzzle_str


def save_puzzle(filepath, puzzle):
    """!
    @brief Save a 9x9 numpy array as a sudoku puzzle to a given file.
    """
    # check that we are saving to a text file
    assert filepath.endswith(".txt"), "Filepath must end with .txt"

    # get puzzle as string
    puzzle_str = puzzle_to_string(puzzle)

    # Write the formatted string to the file
    with open(filepath, "w") as file:
        file.write(puzzle_str)


def print_puzzle(puzzle):
    """!
    @brief Prints numpy array as sudoku puzzle
    """
    print(puzzle_to_string(puzzle))
