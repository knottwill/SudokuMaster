Will include:

- Title
- Description + motivation
- Contents (project directory tree & description of folders)
- Installation
- How to run/use the project
- Features
- Frameworks (Languages/Testing/CI/Containerisation)
- Build status / Known bugs / version info (optional)
- Credits

# Sudoku Master

## Description + Motivation

Program to solve 9x9 Sudoku puzzles using the backtracking algorithm, paried with four candidate elimination techniques: 'Naked Singles', 'Hidden Singles', 'Obvious Pairs' (AKA 'Naked Pairs'), 'Pointing Pairs/Triples'.

## Contents

Project directory
```
├── docs
│   └── Doxyfile
├── src
│   ├── engine
│   │   ├── __init__.py
│   │   ├── backtracking.py
│   │   ├── basics.py
│   │   └── elimination.py
│   ├── toolkit
│   │   ├── __init__.py
│   │   ├── generation.py
│   │   ├── input.py
│   │   ├── output.py
│   │   └── validation.py
│   └── solve_sudoku.py
└── tests
│   ├── test_puzzles/
│   ├── __init__.py
│   ├── test_backtracking.py
│   ├── test_basics.py
│   ├── test_elimination.py
│   ├── test_io.py
│   ├── test_solver.py
│   └── test_validation.py
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
└── README.md
```

## Installation

## Accessing data

Must run these commands from the root directory of the project and must run the commands exactly as they are written below (any name changes will cause the script to fail)

```bash
$ mkdir puzzles/
$ curl https://norvig.com/top95.txt --output puzzles/hard.txt
$ curl https://norvig.com/hardest.txt --output puzzles/hardest.txt
$ curl https://projecteuler.net/project/resources/p096_sudoku.txt --output puzzles/easy.txt
$ python convert_data.py
```

## Usage

<b> Warning: </b> Running tests in `tests/test_solver.py` may overwrite and delete solutions of puzzles you have saved in a directory `solutions/`, depending on the filenames. We recommend moving solutions elsewhere if you want to ensure they are untouched.
