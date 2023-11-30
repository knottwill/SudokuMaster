import sys
import numpy as np
from time import time

from toolkit.io import load_puzzle, print_puzzle, save_puzzle
from toolkit.validation import validate_solution
from engine.basics import init_candidates, filler, solvable
from engine.elimination import all_elimination
from engine.backtracking import backtracker

assert len(sys.argv) != 1, "No filepath provided"
assert len(sys.argv) < 4, "Too many arguments provided"

# filepath is passed as argument
filepath = sys.argv[1]

# num_solutions is (optionally) passed as argument
# otherwise, we take num_solutions = 1
if len(sys.argv) == 3:
    assert sys.argv[2].isdigit(), "2nd argument, <num_solutions>, must be an integer"
    num_solutions = int(sys.argv[2])
else:
    num_solutions = 1

# load puzzle
puzzle = load_puzzle(filepath)

# filename (for saving the file after)
filename = filepath.split(".txt")[0].split("/")[-1]

# if puzzle fails to load, stop here
# we don't need to print error message, load_puzzle will do this
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
    savepath = "solutions/" + filename + "_solution.txt"
    save_puzzle(savepath, filled_puzzle)
    print(f"Solution saved in {savepath}")
    sys.exit()  # stop running if solution found
assert (
    message == "Solution is Unfilled"
), f"Puzzle filled by candidate elimination is invalid: {message}"

# ------------------------
# Brute force (backtracking)
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
    message = validate_solution(puzzle, solution)
    assert message == "Valid", f"Solution incorrect: {message}"

    # print solution
    print(f"Solution Found in {post_backtracking - start: .3}s\n")
    print("Using candidate elimination and backtracking\n")
    print_puzzle(solution)
    savepath = "solutions/" + filename + "_solution.txt"
    save_puzzle(savepath, solution)
    print(f"Solution saved in {savepath}")

else:
    print(f"{len(solutions)} Solution(s) Found in {post_backtracking - start: .3}s\n")
    for i, solution in enumerate(solutions):
        message = validate_solution(puzzle, solution)
        assert message == "Valid", f"Solution incorrect: {message}"

        # print & save solutions
        print_puzzle(solution)
        savepath = "solutions/" + filename + "_solution" + str(i + 1) + ".txt"
        save_puzzle(savepath, solution)
        print(f"Solution saved in {savepath}")
