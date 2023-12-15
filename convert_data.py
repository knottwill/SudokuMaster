import numpy as np
import os

from src.toolkit.output import save_puzzle
from src.toolkit.input import parse_sudoku_string

# asserting the files to convert have been downloaded
assert os.path.exists("puzzles/easy.txt"), "Project Euler puzzles not found"
assert os.path.exists("puzzles/hard.txt"), "Peter Norvig's 95 hard puzzles not found"
assert os.path.exists(
    "puzzles/hardest.txt"
), "Peter Norvig's 11 hardest puzzles not found"

# --------------------
# Converting project euler puzzles
# -------------------

with open("puzzles/easy.txt", "r") as file:
    easy_content = file.read()

# split it up into grids
grids = easy_content.split("Grid ")
grids.pop(0)

# assert there are 50 puzzles
assert (
    len(grids) == 50
), "Project Euler's 50 puzzles not found inside 'puzzles/easy.txt'"

for grid in grids:
    # Splitting the grid number and the grid content
    grid_number, grid_content = grid.split("\n", 1)

    output = parse_sudoku_string(grid_content)

    if isinstance(output, np.ndarray):
        puzzle = output
        save_puzzle("puzzles/easy/easy_" + grid_number + ".txt", puzzle)

# --------------------
# Converting Peter Norvig's "top95" and "hardest" puzzles
# -------------------


# function converts the puzzle strings (in Peter Norvig's format) to arrays
def convert_to_array(puzzle_string):
    return np.array(list(puzzle_string.replace(".", "0"))).astype(int).reshape((9, 9))


# load 'hard' puzzles
with open("puzzles/hard.txt", "r") as file:
    hard_content = file.read()

# get list of puzzle strings
hard_strings = hard_content.split("\n")
hard_strings = [p for p in hard_strings if p != ""]
hard_puzzles = [convert_to_array(p) for p in hard_strings]

# assert there are 95 hard puzzles
assert (
    len(hard_puzzles) == 95
), "Peter Norvig's 95 hard puzzles not found inside 'puzzles/hard.txt'"

# save each puzzle to its own file
for i, puzzle in enumerate(hard_puzzles):
    num = str(i + 1)
    num = num if len(num) == 2 else "0" + num
    save_puzzle("puzzles/hard/hard_" + num + ".txt", puzzle)

# identical, but for 'hardest' puzzles
with open("puzzles/hardest.txt", "r") as file:
    hardest_content = file.read()

hardest_strings = hardest_content.split("\n")
hardest_strings = [p for p in hardest_strings if p != ""]
hardest_puzzles = [convert_to_array(p) for p in hardest_strings]

assert (
    len(hardest_puzzles) == 11
), "Peter Norvig's 11 hardest puzzles not found inside 'puzzles/hardest.txt"

for i, puzzle in enumerate(hardest_puzzles):
    num = str(i + 1)
    num = num if len(num) == 2 else "0" + num
    save_puzzle("puzzles/hardest/hardest_" + num + ".txt", puzzle)


# --------------------
# Saving the 'world's hardest puzzles'
# -------------------

# Worlds hardest puzzle, by Arto Inkala in 2012
# https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html
hardest_2012 = np.array(
    [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]
)
save_puzzle("puzzles/worlds_hardest_2012.txt", hardest_2012)

# Previous worlds hardest puzzle, by Arto Inkala in 2010
# https://www.dailymail.co.uk/news/article-1304222/It-took-months-create-long-crack--worlds-hardest-Sudoku.html
hardest_2010 = np.array(
    [
        [0, 0, 5, 3, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 2, 0],
        [0, 7, 0, 0, 1, 0, 5, 0, 0],
        [4, 0, 0, 0, 0, 5, 3, 0, 0],
        [0, 1, 0, 0, 7, 0, 0, 0, 6],
        [0, 0, 3, 2, 0, 0, 0, 8, 0],
        [0, 6, 0, 5, 0, 0, 0, 0, 9],
        [0, 0, 4, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 9, 7, 0, 0],
    ]
)
save_puzzle("puzzles/worlds_hardest_2010.txt", hardest_2010)
