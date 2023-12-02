"""! @file elimination.py
@brief Module contains all tools for eliminating candidates of squares in Sudoku puzzles

@details This module contains four candidate elimination techniques: 'Naked Singles',
'Hidden Singles', 'Obvious Pairs', 'Pointing Pairs/Triples'. Each technique takes
a candidates grid as input, and returns the modified grid (after eliminating
candidates). The module also contains a function to combine all four techniques
and loop them until no more candidates can be eliminated.

@author Created by W.D Knottenbelt
"""
import numpy as np
import copy


def naked_singles_elimination(candidates):
    """!
    @brief Eliminate candidates using the naked singles technique.

    @details Naked Singles technique: Function finds squares that
    only have a single candidate, then that candidate can be eliminated
    from all other squares in the same row, column and block

    Reference: https://sudoku.com/sudoku-rules/obvious-singles/

    @param candidates (numpy.ndarray) The candidates grid as a numpy array.

    @return Updated candidates grid
    """
    # check candidates grid is of the correct type and shape
    assert isinstance(candidates, np.ndarray) and candidates.dtype == object
    assert candidates.shape == (9, 9)

    for i in range(9):
        for j in range(9):
            if len(candidates[i, j]) == 1:
                # extract the single candidate
                value = list(candidates[i, j])[0]

                # eliminate this candidate from all squares in the same row
                for c in range(9):
                    if c != j:
                        candidates[i, c].discard(value)

                # eliminate this candidate from all squares in the same column
                for r in range(9):
                    if r != i:
                        candidates[r, j].discard(value)

                # eliminate this candidate from all squares in the same block
                block_i = 3 * (i // 3)  # row index of top left square in block
                block_j = 3 * (j // 3)  # col index of top left square in block
                for r in range(block_i, block_i + 3):
                    for c in range(block_j, block_j + 3):
                        if r != i or c != j:
                            candidates[r, c].discard(value)

    return candidates


def unique_in_group(group, current_candidates):
    """!
    @brief Check if any number in a set of numbers are unique in a group

    @details This function checks if any of the numbers in current_candidates
    appear exactly once in the group (which is typically a subset of the
    candidate grid, eg. One row). If so, we return the number that is unique.
    If not, we return None.

    @param group (numpy.ndarray) The group of squares (part of the candidate grid)
    @param current_candidates (set) The set of numbers to consider uniqueness in group

    @return Unique candidate or None (if no unique candidate is found).
    """
    # count how many times each candidate in current_candidates
    # appears in the group
    candidate_counts = {}
    for candidate in current_candidates:
        for square in group:
            # if candidate is found in square then we increase the count by 1
            if candidate in square:
                if candidate in candidate_counts:
                    candidate_counts[candidate] += 1
                else:
                    candidate_counts[candidate] = 1

    # Find a candidate in current_candidates that appears only once in the group
    for candidate in current_candidates:
        if candidate_counts[candidate] == 1:
            return candidate
    return None


def hidden_singles_elimination(candidates):
    """!
    @brief Eliminate candidates using the hidden singles technique.

    @details Hidden Singles technique: If a particular number is a
    candidate of only one square in an entire row, column or block,
    even though the square has other candidates, then that number
    becomes the only candidate of that square.

    Reference: https://sudoku.com/sudoku-rules/hidden-singles/

    @param candidates (numpy.ndarray) The candidates grid as a numpy array.

    @return Updated candidates grid
    """
    # check candidates grid is of the correct type and shape
    assert isinstance(candidates, np.ndarray) and candidates.dtype == object
    assert candidates.shape == (9, 9)

    for i in range(9):
        for j in range(9):
            current_candidates = candidates[i, j]

            # we only check if squares with multiple candidates contain hidden singles
            # (if it is the sole candidate then it isn't very 'hidden')
            if len(current_candidates) > 1:
                # check if any current candidates are unique in row
                # if we find a candidate is unique, it becomes the sole candidate
                unique_in_row = unique_in_group(candidates[i, :], current_candidates)
                if unique_in_row:
                    candidates[i, j] = {unique_in_row}
                    continue

                # same for column
                unique_in_col = unique_in_group(candidates[:, j], current_candidates)
                if unique_in_col:
                    candidates[i, j] = {unique_in_col}
                    continue

                # same for block
                block_i = 3 * (i // 3)
                block_j = 3 * (j // 3)
                block = candidates[
                    block_i : block_i + 3, block_j : block_j + 3
                ].flatten()
                unique_in_block = unique_in_group(block, current_candidates)
                if unique_in_block:
                    candidates[i, j] = {unique_in_block}

    return candidates


def obvious_pairs_elimination(candidates):
    """!
    @brief Eliminate candidates using the obvious pairs technique (AKA naked pairs)

    @details Obvious Pairs technique: If two squares in the same row, column or block
    have exactly two candidates, and they are the same two candidates for both squares,
    then those two candidates are be eliminated from all of squares in that row,
    column or block.

    Reference: https://sudoku.com/sudoku-rules/obvious-pairs/

    @param candidates (numpy.ndarray) The candidates grid as a numpy array.

    @return Updated candidates grid
    """
    # check candidates grid is of the correct type and shape
    assert isinstance(candidates, np.ndarray) and candidates.dtype == object
    assert candidates.shape == (9, 9)

    # search every square in grid
    for i in range(9):
        for j in range(9):
            # check if the current square has exactly two candidates.
            if len(candidates[i, j]) == 2:
                pair = candidates[i, j]

                # check for identical pair in the same row.
                for c in range(9):
                    if c != j and candidates[i, c] == pair:
                        # eliminate the pair from all other squares in the same row.
                        for eliminate_c in range(9):
                            if eliminate_c != j and eliminate_c != c:
                                candidates[i, eliminate_c] -= pair

                # check for identical pair in the same column.
                for r in range(9):
                    if r != i and candidates[r, j] == pair:
                        # eliminate the pair from all other squares in the same column.
                        for eliminate_r in range(9):
                            if eliminate_r != i and eliminate_r != r:
                                candidates[eliminate_r, j] -= pair

                # check for identical pair in the same block.
                block_i, block_j = 3 * (i // 3), 3 * (j // 3)
                for r in range(block_i, block_i + 3):
                    for c in range(block_j, block_j + 3):
                        if (r != i or c != j) and candidates[r, c] == pair:
                            # eliminate the pair from all other squares in the same block.
                            for eliminate_r in range(block_i, block_i + 3):
                                for eliminate_c in range(block_j, block_j + 3):
                                    if (eliminate_r != i or eliminate_c != j) and (
                                        eliminate_r != r or eliminate_c != c
                                    ):
                                        candidates[eliminate_r, eliminate_c] -= pair

    return candidates


def pointing_elimination(candidates):
    """!
    @brief Eliminate candidates using the pointing pairs/triples technique

    @details Pointing Pairs/Triples technique: Checks each block to see if a
    candidate number appears only in a single row or column within that block.
    If so, that candidate can be eliminated from the rest of the row or column
    outside of the block, since it must appear in the block.

    Reference 1: https://sudoku.com/sudoku-rules/pointing-pairs/
    Reference 2: https://sudoku.com/sudoku-rules/pointing-triples/

    @param candidates (numpy.ndarray) The candidates grid as a numpy array.

    @return Updated candidates grid
    """
    # check candidates grid is of the correct type and shape
    assert isinstance(candidates, np.ndarray) and candidates.dtype == object
    assert candidates.shape == (9, 9)

    # take copy of candidates grid to avoid modifying the original
    # candidates = copy.deepcopy(candidates)

    # loop over each block
    for block_i in range(0, 9, 3):
        for block_j in range(0, 9, 3):
            # for each number, find which rows and columns they are in (within the block)
            for num in range(1, 10):
                rows_with_num = set()
                cols_with_num = set()

                # loop over squares within the block to find the rows and columns where the number appears.
                for i in range(block_i, block_i + 3):
                    for j in range(block_j, block_j + 3):
                        if num in candidates[i, j]:
                            rows_with_num.add(i)
                            cols_with_num.add(j)

                # apply pointing pairs/triples technique for rows
                if len(rows_with_num) == 1:
                    # row index containing pointing pairs/triples
                    row = list(rows_with_num)[0]
                    # discard num from the rest of the row
                    for c in range(9):
                        if c < block_j or c >= block_j + 3:
                            candidates[row, c].discard(num)

                # apply pointing pairs/triples technique for columns
                if len(cols_with_num) == 1:
                    # column index containing pointing pairs/triples
                    col = list(cols_with_num)[0]
                    # discard num from rest of column
                    for r in range(9):
                        if r < block_i or r >= block_i + 3:
                            candidates[r, col].discard(num)

    return candidates


def all_elimination(candidates):
    """!
    @brief Repeated application of all four elimination techniques

    @details Applies the following candidate elimination techniques sequentially to the
    candidates grid in a loop until no more candidates can be eliminated using these
    techniques: 'Naked Singles', 'Hidden Singles', 'Obvious Pairs', 'Pointing Pairs/Triples'

    @param candidates (numpy.ndarray) The candidates grid as a numpy array.

    @return Updated candidates grid
    """
    # check candidates grid is of the correct type and shape
    assert isinstance(candidates, np.ndarray) and candidates.dtype == object
    assert candidates.shape == (9, 9)

    # Take copy of candidates grid to avoid mutating the original
    candidates = copy.deepcopy(candidates)

    # Apply all elimination techniques until candidates grid stops changing
    old_candidates = None
    while not np.array_equal(candidates, old_candidates):
        old_candidates = copy.deepcopy(candidates)
        candidates = naked_singles_elimination(candidates)
        candidates = hidden_singles_elimination(candidates)
        candidates = obvious_pairs_elimination(candidates)
        candidates = pointing_elimination(candidates)

    return candidates
