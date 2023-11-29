import sys
import numpy as np
from time import time

from toolkit.io import load_puzzle, print_puzzle
from toolkit.validation import validate_solution
from engine.basics import init_candidates, filler, solvable
from engine.elimination import all_elimination
from engine.backtracking import backtracker

assert len(sys.argv) != 1, "No filepath provided"
assert len(sys.argv) < 3, "Too many files provided"
assert len(sys.argv) == 2

filepath = sys.argv[1]
puzzle = load_puzzle(filepath)

# if puzzle fails to load, stop here
# we don't need to print anything, as load_puzzle will do this
if puzzle is None:
    sys.exit()

orig_puzzle = puzzle.copy()  # taking copy in case puzzle is modified
start = time()  # timing

# --------------------
# Candidate Elimination
# --------------------

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
    print(f"Solution Found in {post_elimination - start: .3}s\n")
    print("Using candidate elimination alone\n")
    print_puzzle(filled_puzzle)
    sys.exit()  # stop running if solution found
assert (
    message == "Solution is Unfilled"
), f"Puzzle filled by candidate elimination is invalid: {message}"

# ------------------------
# Brute force (backtracking)
# ------------------------

# perform backtracking
solution = backtracker(puzzle, candidates)
post_backtracking = time()

# check if puzzle is unsolvable
if isinstance(solution, str) and solution == "UNSOLVABLE":
    print("Puzzle is Unsolvable")
    sys.exit()

# assert original puzzle has not been modified
assert np.array_equal(puzzle, orig_puzzle), "Original puzzle has been modified"

# if we get here, solution must have been found
message = validate_solution(puzzle, solution)
assert message == "Valid", f"Solution incorrect: {message}"

# print solution
print(f"Solution Found in {post_backtracking - start: .3}s\n")
print("Using candidate elimination and backtracking\n")
print_puzzle(solution)
