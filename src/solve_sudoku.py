"""!@file solve_sudoku.py
@brief Python script to solve Sudoku puzzles
"""

import sys
import numpy as np
from time import time

from toolkit.input import load_puzzle
from toolkit.output import print_puzzle, save_puzzle
from toolkit.validation import validate_solution
from engine.basics import init_candidates, filler, solvable
from engine.elimination import all_elimination
from engine.backtracking import backtracker

# --------------------------
# Loading puzzle & Performing Checks
# --------------------------

assert len(sys.argv) != 1, "No filepath provided"
assert len(sys.argv) < 4, "Too many arguments provided"

# filepath is passed as argument
filepath = sys.argv[1]

# num_solutions is (optionally) passed as argument (otherwise, default is 1)
if len(sys.argv) == 3:
    assert sys.argv[2].isdigit(), "2nd argument, <num_solutions>, must be an integer"
    num_solutions = int(sys.argv[2])
else:
    num_solutions = 1

# load puzzle
puzzle = load_puzzle(filepath)
# if puzzle fails to load, stop here
if puzzle is None:
    sys.exit()  # error message will be handled by load_puzzle

# filename (for saving the solution)
filename = filepath.split(".txt")[0].split("/")[-1]

orig_puzzle = puzzle.copy()  # taking copy in case puzzle is modified

start = time()  # timing

# ------------------------
# Initial Candidate Elimination
# ------------------------

# initialise candidates grid
candidates = init_candidates(puzzle)

# perform candidate elimination techniques
candidates = all_elimination(candidates)

# check if puzzle is solvable
if not solvable(candidates):
    print("Puzzle is Unsolvable")
    sys.exit()

# fill in puzzle as much as possible
filled_puzzle = filler(puzzle, candidates)
post_elimination = time()

# check if solution has been already found
message = validate_solution(puzzle, filled_puzzle)
if message == "Valid":
    # print solution
    print(f"Solution Found in {post_elimination - start: .3}s\n")
    print("Using candidate elimination alone\n")
    print_puzzle(filled_puzzle)
    # save solution
    savepath = "./solutions/" + filename + "_solution.txt"
    save_puzzle(savepath, filled_puzzle)
    print(f"Solution saved in {savepath}")
    sys.exit()  # stop running if solution found

# if we get here, filled_puzzle should contain empty squares
# but should be valid / compatible with original puzzle
assert (
    message == "Solution is Unfilled"
), f"Puzzle after candidate elimination is invalid: {message}"

# ------------------------
# Backtracking (Brute force search)
# ------------------------

# perform backtracking
solutions = backtracker(puzzle, candidates, num_solutions)
post_backtracking = time()

# check if puzzle is unsolvable
if isinstance(solutions, str) and solutions == "UNSOLVABLE":
    print("Puzzle is Unsolvable")
    sys.exit()

# assert original puzzle has not been modified
assert np.array_equal(puzzle, orig_puzzle), "Original puzzle has been modified"

# if we get here, solution(s) must have been found
if num_solutions == 1:
    solution = solutions

    # assert solution is valid
    message = validate_solution(puzzle, solution)
    assert message == "Valid", f"Solution incorrect: {message}"

    # print solution
    print(f"Solution Found in {post_backtracking - start: .3}s\n")
    print("Using candidate elimination and backtracking\n")
    print_puzzle(solution)
    # save solution
    savepath = "./solutions/" + filename + "_solution.txt"
    save_puzzle(savepath, solution)
    print(f"Solution saved in {savepath}\n")

else:
    # print & save all solutions
    print(f"{len(solutions)} Solution(s) Found in {post_backtracking - start: .3}s\n")
    print("Using candidate elimination and backtracking\n")
    for i, solution in enumerate(solutions):
        # assert solution is valid
        message = validate_solution(puzzle, solution)
        assert message == "Valid", f"Solution incorrect: {message}"

        # print solution
        print_puzzle(solution)
        # save solution
        savepath = "./solutions/" + filename + "_solution" + str(i + 1) + ".txt"
        save_puzzle(savepath, solution)
        print(f"Solution saved in {savepath}")
