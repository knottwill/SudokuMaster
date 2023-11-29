import sys

from toolkit.io import load_puzzle, print_puzzle
from toolkit.validation import validate_solution
from engine.basics import init_candidates, filler, solvable
from engine.elimination import all_elimination
from engine.backtracking import backtracker

assert len(sys.argv) != 1, "No filepath provided"

assert len(sys.argv) == 2, "Too many files provided"

filepath = sys.argv[1]
orig_puzzle = load_puzzle(filepath)

# taking copy in case puzzle is modified
puzzle = orig_puzzle.copy()

# initialise candidates grid
candidates = init_candidates(puzzle)

# perform candidate elimination techniques
candidates = all_elimination(candidates)

# check if puzzle is solvable
if not solvable(candidates):
    print("Puzzle is unsolvable")
    sys.exit()

# fill in puzzle as much as possible
filled_puzzle = filler(puzzle, candidates)

# check if solution has been already found
message = validate_solution(puzzle, filled_puzzle)
if message == "Valid":
    print("Solution Found:\n")
    print_puzzle(filled_puzzle)
    sys.exit()  # stop running if solution found

# if we get here, solution has not been found
# hence the filled_puzzle should contain 0's
assert message == "Solution is Unfilled"

print("Solution not found using candidate elimination alone, brute force needed\n")

# perform backtracking
solution = backtracker(puzzle, candidates)

if isinstance(solution, str) and solution == "UNSOLVABLE":
    print("Puzzle is unsolvable")
    sys.exit()

# if we get here, solution must have been found
message = validate_solution(puzzle, solution)
assert message == "Valid", f"Solution incorrect: {message}"

# print solution
print("Solution Found:\n")
print_puzzle(solution)
