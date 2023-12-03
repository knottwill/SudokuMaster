# Sudoku Master

&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.11.5-blue.svg)
&nbsp;&nbsp;&nbsp;&nbsp;
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)


This program was developed to solve 9x9 Sudoku puzzles using the backtracking algorithm, paired with four candidate elimination techniques: 'Naked Singles', 'Hidden Singles', 'Obvious Pairs' (AKA 'Naked Pairs'), 'Pointing Pairs/Triples'.

<details><summary><b>View Project Structure</b></summary>

    ├── docs
    │   └── Doxyfile            # auto-documentation configuration
    ├── src
    │   ├── engine              # core solving algorithms
    │   │   ├── __init__.py
    │   │   ├── backtracking.py # backtracking algorithm
    │   │   ├── basics.py       # basic tools core to the solvers
    │   │   └── elimination.py  # candidate elimination techniques
    │   ├── toolkit             # utilities for loading, saving & manipulating puzzles
    │   │   ├── __init__.py
    │   │   ├── generation.py   # generating puzzles
    │   │   ├── input.py        # handling inputs to program
    │   │   ├── output.py       # handle outputs of program (including visualisation)
    │   │   └── validation.py   # validation tools
    │   └── solve_sudoku.py     # main executable script
    └── tests                   # testing suite
    │   ├── test_puzzles/       # puzzle examples used in testing
    │   ├── __init__.py
    │   ├── test_backtracking.py
    │   ├── test_basics.py
    │   ├── test_elimination.py
    │   ├── test_generation.py
    │   ├── test_io.py
    │   ├── test_solver.py
    │   └── test_validation.py
    ├── .gitignore              # specifies untracked files to ignore
    ├── .pre-commit-config.yaml # config for pre-commit hooks
    ├── Dockerfile              # containerisation instructions
    ├── LICENSE
    ├── README.md
    ├── convert_data.py         # script for data conversion
    └── environment.yml         # environment specifications

</details>

## Table of Contents

 * [Features](#features)
 * [Installation](#installation)
 * [Usage](#usage)
    - [Solving Puzzles](#solving-puzzles)
    - [Visualisation](#visualisation)
    - [Puzzle Generation](#puzzle-generation)
* [Frameworks](#frameworks)
* [Credits](#credits)

## Features

1. <b>Comprehensive Sudoku Solving Engine</b>
    - Four candidate elimination techniques ('Naked Singles', 'Hidden Singles', 'Obvious Pairs', 'Pointing Pairs/Triples')
    - Backtracking algorithm (enhanced with candidate elimination to reduce search space)

2. <b>Input/Output handling and visualisation</b>
    - Loading puzzles from text files
    - Saving puzzles as text files
    - Intuitive visualisation of puzzles and candidate grids (printed to console)

3. <b>Extensive Validation and Testing</b>
    - Validating puzzles and solutions to puzzles
    - Rigorous tests of all core components to ensure reliability

4. <b>Puzzle Generation</b>
    - Generation of example puzzles which can solved by repeatedly filling in 'Naked Singles'

## Installation

First, clone the repository:

```bash
$ git clone https://gitlab.developers.cam.ac.uk/phy/data-intensive-science-mphil/c1_assessment/wdk24.git
$ cd wdk24
```

<b>Method 1: Using Docker</b>

Simply build the docker image (using `Dockerfile`) and run a container:
```bash
$ docker build -t <image-name> .
$ docker run -ti <image-name>
```

<b>Method 2: Using Conda</b>

Set up the environment using the `environment.yml` file:

```bash
$ conda env create -f environment.yml -n <environment-name>
$ conda activate <environment-name>
```

Alternatively, create a new environment and install the dependancies manually: (although, new versions of these packages could cause conflics in the project, so be warned.)

```bash
$ conda install numpy black flake8 pytest pre-commit line_profiler
```

To access all puzzles used for evaluation of algorithms during development, run these commands from the root directory:

```bash
$ mkdir puzzles/
$ curl https://norvig.com/top95.txt --output puzzles/hard.txt
$ curl https://norvig.com/hardest.txt --output puzzles/hardest.txt
$ curl https://projecteuler.net/project/resources/p096_sudoku.txt --output puzzles/easy.txt
$ python convert_data.py
```

This is not needed when using method 1 since `Dockerfile` will do this automatically.

<b>Test Installation (recommended)</b>

After installation, check everything is working by running the testing suite:
```bash
$ pytest
```

## Usage

> **Warning**
> Running the tests in `tests/test_solver.py` may overwrite solutions saved in `solutions/`. Backup your solutions before running tests.

### Solving Puzzles

To solve a Sudoku puzzle, navigate to the root project directory and use the following command:
```bash
$ python src/solve_sudoku.py <file-containing-puzzle> [<num-solutions>]
```
Arguments:
- `<file-containing-puzzle>`: Specify the path to a text file containing the Sudoku puzzle you want to solve. The file should have a valid Sudoku puzzle format.

<details><summary><b>View valid Sudoku puzzle format</b></summary>

    003|020|600
    900|305|001
    001|806|400
    ---+---+---
    008|102|900
    700|000|008
    006|708|200
    ---+---+---
    002|609|500
    800|203|009
    005|010|300
</details>
<br>

- `<num-solutions>` (optional): Specify the number of solutions you want to find. If not provided, the default value is 1. If you specify more solutions than are possible, then all available solutions will be found.

After running the command, the program will process the Sudoku puzzle provided. If solutions are found, they will be printed to the console and saved in `solutions/`.

<details><summary><b>View example usage 1</b></summary>

Finding a single solution:

    $ python src/solve_sudoku.py puzzles/worlds_hardest_2010.txt
    Solution Found in  1.09s

    Using candidate elimination and backtracking

    1 4 5 |3 2 7 |6 9 8
    8 3 9 |6 5 4 |1 2 7
    6 7 2 |9 1 8 |5 4 3
    ------+------+------
    4 9 6 |1 8 5 |3 7 2
    2 1 8 |4 7 3 |9 5 6
    7 5 3 |2 9 6 |4 8 1
    ------+------+------
    3 6 7 |5 4 2 |8 1 9
    9 8 4 |7 6 1 |2 3 5
    5 2 1 |8 3 9 |7 6 4

    Solution saved in ./solutions/worlds_hardest_2010_solution.txt
</details>

<details><summary><b>View example usage 2</b></summary>

Finding multiple solutions:

    $ python src/solve_sudoku.py tests/test_puzzles/10_solutions.txt 3
    3 Solution(s) Found in  0.262s

    Using candidate elimination and backtracking

    5 9 4 |1 6 7 |8 3 2
    6 1 8 |2 3 9 |5 7 4
    3 2 7 |8 5 4 |1 6 9
    ------+------+------
    2 8 9 |7 1 6 |3 4 5
    1 7 5 |3 4 8 |2 9 6
    4 3 6 |5 9 2 |7 8 1
    ------+------+------
    7 6 2 |4 8 1 |9 5 3
    8 4 3 |9 2 5 |6 1 7
    9 5 1 |6 7 3 |4 2 8

    Solution saved in ./solutions/10_solutions_solution1.txt

    5 9 4 |1 6 7 |8 3 2
    6 1 8 |2 3 9 |5 7 4
    3 2 7 |8 5 4 |1 6 9
    ------+------+------
    2 8 9 |7 1 6 |3 4 5
    1 7 5 |3 4 8 |2 9 6
    4 3 6 |5 9 2 |7 8 1
    ------+------+------
    7 6 2 |4 8 5 |9 1 3
    8 4 3 |9 2 1 |6 5 7
    9 5 1 |6 7 3 |4 2 8

    Solution saved in ./solutions/10_solutions_solution2.txt

    5 9 4 |1 6 7 |8 3 2
    6 1 8 |2 3 9 |5 7 4
    2 3 7 |4 5 8 |1 6 9
    ------+------+------
    1 8 9 |7 2 6 |3 4 5
    3 7 5 |8 4 1 |2 9 6
    4 2 6 |3 9 5 |7 8 1
    ------+------+------
    7 6 2 |5 8 4 |9 1 3
    8 4 3 |9 1 2 |6 5 7
    9 5 1 |6 7 3 |4 2 8

    Solution saved in ./solutions/10_solutions_solution3.txt
</details>

### Visualisation

Print intuitive visualisations of puzzles and their respective candidate grids to the console.

<details><summary><b>View example usage</b></summary>

```bash
$ python
>>> from src.toolkit.input import load_puzzle
>>> from src.toolkit.output import print_puzzle, print_candidates
>>> puzzle = load_puzzle('puzzles/worlds_hardest_2010.txt')
>>> print_puzzle(puzzle)
0 0 5 |3 0 0 |0 0 0
8 0 0 |0 0 0 |0 2 0
0 7 0 |0 1 0 |5 0 0
------+------+------
4 0 0 |0 0 5 |3 0 0
0 1 0 |0 7 0 |0 0 6
0 0 3 |2 0 0 |0 8 0
------+------+------
0 6 0 |5 0 0 |0 0 9
0 0 4 |0 0 0 |0 3 0
0 0 0 |0 0 9 |7 0 0

>>> from src.engine.basics import init_candidates
>>> candidates = init_candidates(puzzle)
>>> print_candidates(candidates)
1269      249       5         | 3         24689     24678     | 14689     14679     1478
8         349       169       | 4679      4569      467       | 1469      2         1347
2369      7         269       | 4689      1         2468      | 5         469       348
----------------------------------------------------------------------------------------------
4         289       26789     | 1689      689       5         | 3         179       127
259       1         289       | 489       7         348       | 249       459       6
5679      59        3         | 2         469       146       | 149       8         1457
----------------------------------------------------------------------------------------------
1237      6         1278      | 5         2348      123478    | 1248      14        9
12579     2589      4         | 1678      268       12678     | 1268      3         1258
1235      2358      128       | 1468      23468     9         | 7         1456      12458
```
</details>

### Puzzle generation

You can generate puzzles using the functionality in `toolkit/generation.py`. These puzzles can be solved by repeatedly filling in 'Naked Singles'. There is no option to generate more challenging puzzles.

<details><summary><b>View example usage</b></summary>

```bash
$ python
>>> from src.toolkit.generation import generate_singles
>>> from src.toolkit.output import save_puzzle
>>> puzzle = generate_singles()
>>> save_puzzle('puzzles/my_puzzle.txt', puzzle)
```
</details>

## Frameworks

- <b>Programming Languages: </b> Python was the primary language used for development. Ensure you have Python version 3.11.5 or higher installed on your system.
- <b>Testing Framework:</b> `pytest` was used for writing and running tests.

- <b>Continuous Integration (CI): </b> Pre-commit hooks were configured using `.pre-commit-config.yaml`. Ensure you have `pre-commit` installed

- <b>Containerization: </b> Docker was used for creating a consistent development environment. The `Dockerfile` in the root directory contains instructions to build a Docker image for the project.

- <b>Documentation: </b> Doxygen used for auto-generated code documentation. Configured via the `Doxyfile` in the `docs/` directory.

To generate documentation, ensure you have `doxygen` installed (Eg. `brew install doxygen`). Navigate to `docs/` directory and run the following commands:

```bash
$ doxygen
$ cd latex
$ make
$ open refman.pdf
```

## Credits

This project was developed by William Knottenbelt. Special thanks to [sudoku.com](https://sudoku.com/sudoku-rules/) and [computerphile](https://www.youtube.com/watch?v=G_UYXzGuqvM) for guidance on Sudoku solving techniques.

#### Sources of Testing Puzzles
- **Peter Norvig's Sudoku Solver**: Many of the testing puzzles for this project were sourced from Peter Norvig's [famous essay on Sudoku solving](https://norvig.com/sudoku.html).
- **Project Euler**: 50 puzzles were also sourced from Project Euler's [Problem 96](https://projecteuler.net/index.php?section=problems&id=96).
- **World's Hardest Puzzles**: The two "hardest" Sudoku puzzles in the world were also used for evaluation during development. These were devised by Dr Arto Inkala in [2010](https://www.dailymail.co.uk/news/article-1304222/It-took-months-create-long-crack--worlds-hardest-Sudoku.html) and [2012](https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html)

I extend my gratitude to these sources for providing high-quality, challenging puzzles that have been instrumental in testing and refining this Sudoku solver.
