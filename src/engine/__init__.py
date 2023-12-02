"""!@package engine
@brief Package containing all functionality for finding solutions of Sudoku puzzles

@details This packages contains all tools which are directly related to the solving
of Sudoku Puzzles. The solving algorithms implemented in this package include
backtracking (a brute force approach), and four candidate elimination techniques;
namely 'Naked Singles', 'Hidden Singles', 'Obvious Pairs', 'Pointing Pairs/Triples'.
There are two main data objects used in this package. The first is `puzzle` - a
9x9 NumPy array, where each element is the number occupying that square of the puzzle,
or 0 representing an empty square. The second is `candidates` - a 9x9 NumPy array
where each element is a set of numbers representing the possible candidates for that
square of the puzzle.
"""
