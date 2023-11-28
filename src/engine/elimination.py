"""!
@brief Module contains all functionality eliminating candidates from the candidates grid
"""
import copy


def naked_singles_elimination(candidates):
    """
    @brief Eliminate candidates using the naked singles technique.
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
