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
if puzzle == 0:
    sys.exit()

orig_puzzle = puzzle.copy()  # taking copy in case puzzle is modified

# timing
t0 = time()

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
t1 = time()

# check if solution has been already found
message = validate_solution(puzzle, filled_puzzle)
if message == "Valid":
    print(f"Solution Found in {t1 - t0: .3}s\n")
    print_puzzle(filled_puzzle)
    sys.exit()  # stop running if solution found

# if we get here, solution has not been found
# hence the filled_puzzle should contain 0's
assert message == "Solution is Unfilled"

print("Solution not found using candidate elimination alone, brute force needed\n")

# perform backtracking
solution = backtracker(puzzle, candidates)
t2 = time()

if isinstance(solution, str) and solution == "UNSOLVABLE":
    print("Puzzle is Unsolvable")
    sys.exit()

assert np.array_equal(puzzle, orig_puzzle), "Puzzle should not have been modified"

# if we get here, solution must have been found
message = validate_solution(puzzle, solution)
assert message == "Valid", f"Solution incorrect: {message}"

# print solution
print(f"Solution Found in {t2 - t0: .3}s\n")
print_puzzle(solution)
