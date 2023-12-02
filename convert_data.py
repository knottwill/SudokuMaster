import numpy as np

from src.toolkit.output import save_puzzle
from src.toolkit.input import parse_sudoku_string

# --------------------
# Converting project euler puzzles
# -------------------

with open("puzzles/easy.txt", "r") as file:
    easy_content = file.read()

# split it up into grids
grids = easy_content.split("Grid ")
grids.pop(0)

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

for i, puzzle in enumerate(hardest_puzzles):
    num = str(i + 1)
    num = num if len(num) == 2 else "0" + num
    save_puzzle("puzzles/hardest/hardest_" + num + ".txt", puzzle)
