def possibilities(puzzle, i, j):
    row = puzzle[i]
    col = puzzle[:, j]

    # getting indices of the top left square in relevant block
    block_i = 3 * (i // 3)  # row index
    block_j = 3 * (j // 3)  # column index

    # getting block
    block = puzzle[block_i : block_i + 3, block_j : block_j + 3].flatten()

    # find all unique integers above 0 in row, col and block
    taken_numbers = set(set(row) | set(col) | set(block)) - set([0])

    # return which numbers are available to the square
    return list(set(range(1, 10)) - taken_numbers)


def singles_filler(puzzle):
    """!
    @brief Fills in 'Naked Singles' (guarantees all hidden singles to be filled too)
    """
    puzzle = puzzle.copy()

    finished = False
    while not finished:
        restart_loop = False
        for i, row in enumerate(puzzle):
            for j, square in enumerate(row):
                # skip square if it is not empty
                if square != 0:
                    continue

                # find which numbers are available to the square
                available_numbers = possibilities(puzzle, i, j)

                # if there are no available numbers, the puzzle is not solvable
                if len(available_numbers) == 0:
                    return "UNSOLVABLE"

                # if there is 1 available number, fill it in
                if len(available_numbers) == 1:
                    puzzle[i, j] = available_numbers[0]
                    # print(f'filled [{i},{j}]')
                    restart_loop = True
                    break

                # if we have reached the end of the puzzle, then there are no
                # more naked singles, hence we are finished
                if (i, j) == (8, 8):
                    finished = True
                    break

        if restart_loop or finished:
            break

    return puzzle
