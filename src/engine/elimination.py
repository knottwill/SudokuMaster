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
    # take copy of candidates grid to avoid modifying the original
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
    # take copy of candidates grid to avoid modifying the original
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


def obvious_pairs_elimination(candidates):
    """
    @brief Eliminate candidates using the obvious pairs technique (AKA naked pairs)

    @details The obvious pairs technique works as follows: If two squares in the
    same row, column or block have exactly two candidates, and they are the same
    two candidates for both squares, then these two candidates can be eliminated
    from all of squares in that row, column or block.

    Reference: https://sudoku.com/sudoku-rules/obvious-pairs/
    """
    # take copy of candidates grid to avoid modifying the original
    candidates = copy.deepcopy(candidates)

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
    """
    @brief Eliminate candidates using the pointing pairs/triples technique

    @details This function applies the pointing pairs/triples technique: It checks each
    block to see if a candidate number appears only in a single row or column within that
    block. If so, that candidate can be eliminated from the rest of the row or column outside
    the block, since it must appear in the block.

    Reference 1: https://sudoku.com/sudoku-rules/pointing-pairs/
    Reference 2: https://sudoku.com/sudoku-rules/pointing-triples/
    """
    # take copy of candidates grid to avoid modifying the original
    candidates = copy.deepcopy(candidates)

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
