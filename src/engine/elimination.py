"""!
@brief Module contains all functionality eliminating candidates from the candidates grid
"""
import copy


def naked_singles_elimination(candidates):
    """
    @brief Eliminate candidates using the naked singles technique.

    @details The naked singles technique works by finding squares that
    only have a single candidate, then that candidate can be eliminated
    from all other squares in the same row, column and block

    Reference: https://sudoku.com/sudoku-rules/obvious-singles/
    """
    candidates = copy.deepcopy(candidates)

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
    @brief Check if numbers in current_candidates are unique in group

    @details This function checks if any of the candidates in
    current_candidates only appear once in group. If so, we
    return the candidate. If not, we return None

    @return candidate (if unique) or None (if not)
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

    @details The hidden singles technique is as follows: If a particular
    number is a candidate of only one square in an entire row, column
    or block, even though that square has other candidates, the square
    must be filled with that number.

    Reference: https://sudoku.com/sudoku-rules/hidden-singles/
    """
    candidates = copy.deepcopy(candidates)

    for i in range(9):
        for j in range(9):
            current_candidates = candidates[i, j]
            # we only check if squares with multiple candidates contain hidden singles
            if len(current_candidates) > 1:
                # check row
                unique_in_row = unique_in_group(candidates[i, :], current_candidates)
                if unique_in_row:
                    candidates[i, j] = {unique_in_row}
                    continue

                # check column
                unique_in_col = unique_in_group(candidates[:, j], current_candidates)
                if unique_in_col:
                    candidates[i, j] = {unique_in_col}
                    continue

                # check block
                block_i = 3 * (i // 3)
                block_j = 3 * (j // 3)
                block = candidates[
                    block_i : block_i + 3, block_j : block_j + 3
                ].flatten()
                unique_in_block = unique_in_group(block, current_candidates)
                if unique_in_block:
                    candidates[i, j] = {unique_in_block}

    return candidates
