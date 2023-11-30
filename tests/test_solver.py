"""
Robust testing for solve_sudoku.py
"""
import subprocess
import os

# path to solver script
path_to_solver = "./src/solve_sudoku.py"

# getting all filepaths of all valid and unsolvable test puzzles
singles_only = "tests/test_puzzles/singles_only/"
easy = "tests/test_puzzles/easy/easy_"
hard = "tests/test_puzzles/hard/hard_"
hardest = "tests/test_puzzles/hardest/hardest_"
unsolvable = "tests/test_puzzles/unsolvable/unsolvable_"

valid_filepaths = []
unsolvable_filepaths = []
for file in ["01.txt", "02.txt", "03.txt"]:
    valid_filepaths.append(singles_only + file)
    valid_filepaths.append(easy + file)
    valid_filepaths.append(hard + file)
    valid_filepaths.append(hardest + file)
    unsolvable_filepaths.append(unsolvable + file)


def test_solver_on_valid():
    # test on all valid test puzzles
    for filepath in valid_filepaths:
        filename = filepath.split(".txt")[0].split("/")[-1]
        result = subprocess.run(
            ["python", path_to_solver, filepath], capture_output=True, text=True
        )
        assert result.stdout.startswith("Solution Found")

        # remove file created
        os.remove("solutions/" + filename + "_solution.txt")

    # if 'solutions/' is now empty, delete it too
    if not os.listdir("solutions/"):
        os.rmdir("solutions/")


def test_multiple_solution():
    filepath = "tests/test_puzzles/10_solutions.txt"
    num_solutions = "4"
    result = subprocess.run(
        ["python", path_to_solver, filepath, num_solutions],
        capture_output=True,
        text=True,
    )
    assert result.stdout.startswith("4 Solution(s) Found")

    # remove files created
    for n in range(1, 5):
        os.remove("solutions/10_solutions_solution" + str(n) + ".txt")

    # if 'solutions/' is now empty, delete it too
    if not os.listdir("solutions/"):
        os.rmdir("solutions/")


def test_solver_on_unsolvable():
    # test on all unsolvable test puzzles
    for filepath in unsolvable_filepaths:
        result = subprocess.run(
            ["python", path_to_solver, filepath], capture_output=True, text=True
        )
        assert result.stdout.startswith("Puzzle is Unsolvable")


def test_solver_on_invalid():
    # invalid file
    filepath = "tests/test_puzzles/invalid/invalid_form.txt"
    result = subprocess.run(
        ["python", path_to_solver, filepath], capture_output=True, text=True
    )
    assert result.stdout.startswith("File contains INVALID FORMAT")

    # invalid puzzle
    filepath = "tests/test_puzzles/invalid/invalid_puzzle.txt"
    result = subprocess.run(
        ["python", path_to_solver, filepath], capture_output=True, text=True
    )
    assert result.stdout.startswith("Puzzle does not comply to sudoku rules")


def test_solver_error_raising():
    # file that doesn't exist
    filepath = "doesnt_exist"
    result = subprocess.run(
        ["python", path_to_solver, filepath], capture_output=True, text=True
    )
    assert result.returncode != 0, "No errors raised when passing non-existant file"

    # no arguments passed
    result = subprocess.run(
        ["python", path_to_solver, filepath], capture_output=True, text=True
    )
    assert result.returncode != 0, "No errors raised when no arguments passed"

    # passing two files as arguments
    filepath1 = "tests/test_puzzles/easy/easy_01.txt"
    filepath2 = "tests/test_puzzles/easy/easy_02.txt"
    result = subprocess.run(
        ["python", path_to_solver, filepath1, filepath2], capture_output=True, text=True
    )
    assert result.returncode != 0, "No errors raised when passing two sudoku files"
