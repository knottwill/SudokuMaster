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

<b> Warning: </b> Running tests in `tests/test_solver.py` may overwrite and delete solutions of puzzles you have saved in a directory `solutions/`, depending on the filenames. We recommend moving solutions elsewhere if you want to ensure they are untouched.

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
