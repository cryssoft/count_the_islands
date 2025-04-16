#!/usr/bin/python3
#
#  Given a matrix of 1s and 0s, count the "islands" that are composed of
#  contiguous sets of 1s (vertically or horizontally).  You're allowed to 
#  simplify by ass-uming that the matrix/map given is entirely surrounded
#  by "water" or 0s.
#
#  Chris Petersen, Crystallized Software, 2025
#
from sys    import argv as g_argv
from typing import Callable


def load_extended_matrix_from_file(p_expected_rows: int, p_expected_columns: int, p_filename: str) -> list[list[int]]:
    """
    Trivial data loader function that encapsulates the matrix of 1s and 0s in a set of
    0s above, left, right, and below the original data.  Does some limited input validation
    along the way.

    NOTE:  This validates the row and column sizing but does not validate the 1s and 0s
    rule that we'll need to make the simulation work.  If this was going to be production
    code anywhere, we'd want to add more validations.
    """
    l_empty: list[list[int]] = []
    l_returns: list[list[int]] = []
    l_row: int = 1

    for l_counter in range(p_expected_columns + 2):
        l_empty.append(0)

    #  Start and end with an empty (all water) row
    l_returns.append(l_empty)
    with open(p_filename, 'r') as l_file:
        for l_line in l_file:
            #  Start and end each row with an empty (water) cell
            l_columns: list[int] = [0]
            l_columns += [int(x) for x in l_line.strip().split(",")]
            l_columns.append(0)
            if (len(l_columns) != (p_expected_columns + 2)):
                raise(ValueError(f"Row {l_row} had invalid length {len(l_columns) - 2} instead of {p_expected_columns}"))
            else:
                l_returns.append(l_columns)
            l_row += 1
    l_returns.append(l_empty)

    if (len(l_returns) != (p_expected_rows + 2)):
        raise(ValueError(f"Data file contained {len(l_returns) - 2} rows instead of {p_expected_rows}"))

    return(l_returns)


def print_matrix(p_heading: str, p_matrix: list[list[int]]) -> None:
    """
    Trivial function to print the curreent values in the matrix as a simple
    set of lists with a spaced heading for clarity.
    """
    print(f"\n{p_heading}\n")
    for l_row in p_matrix:
        print(l_row)

    return


def reduction_visitor(p_row: int, p_column: int, p_matrix: list[list[int]], p_count_remove: list[int]) -> int:
    """
    Simple "visitor" function we'll apply to every cell in the matrix/grid during
    each loop over the grid.  We're only considering up/down/left/right cells as
    adjacent.  Since we're modeling our data as 1s for land and 0s for water, we 
    can just add up the adjacent "land" and see if we have a situation where we
    can mark this land cell as water and move on (change something).
    """
    l_returns: int = 0

    if (p_matrix[p_row][p_column] == 1):
        l_count_adjacent_land: int = p_matrix[p_row - 1][p_column] + p_matrix[p_row][p_column - 1] + p_matrix[p_row][p_column + 1] + p_matrix[p_row + 1][p_column]
        if (l_count_adjacent_land in p_count_remove):
            p_matrix[p_row][p_column] = 0
            l_returns = 1

    return(l_returns)


def apply_visitor_until_stable(p_matrix: list[list[int]], p_visitor: Callable[[int,int,list[list[int]],list[int]],int], p_count_remove: list[int], p_print_intermediate: bool = False) -> None:
    """
    Controller for one kind of visitor pattern -> keep looping while the matrix contents are changing.
    """
    l_count_changes: int = 0
    l_count_loops: int = 0

    while ((l_count_changes != 0) or (l_count_loops == 0)):
        l_count_changes = 0
        for l_row in range(1,(len(p_matrix) - 1)):
            for l_column in range(1,(len(p_matrix[l_row]) - 1)):
                l_count_changes += p_visitor(l_row, l_column, p_matrix, p_count_remove)
        if (p_print_intermediate):
            print_matrix(f"After loop {l_count_loops} changes = {l_count_changes}", p_matrix)
        l_count_loops += 1

    return


def main(p_argv: list[str]) -> None:
    """
    Some of the error handling breaks the "one return" coding policy, but it's a trivial example
    program and our main() returns None anyway.

    Run the two, visitor function through the same, cellular automata-style controller twice with
    slightly different parameters to (1) knock off stragglers/dangling bits from the "islands"
    then (2) reduce the contiguous bits.
    """
    l_count_islands: int = 0

    if (len(p_argv) == 4):
        try:
            l_matrix: list[list[int]] = load_extended_matrix_from_file(int(p_argv[1]), int(p_argv[2]), p_argv[3])
        except FileNotFoundError as l_exception_fnf:
            print(F"File {p_argv[3]} was not found")
            return
        except ValueError as l_exception_value:
            print(l_exception_value)
            return
        print_matrix("Initial data:", l_matrix)
        apply_visitor_until_stable(l_matrix, reduction_visitor, [1], False)      #  Knock off stragglers/peninsulas
        apply_visitor_until_stable(l_matrix, reduction_visitor, [1, 2], False)   #  Knock down contiguous island mass
        print_matrix("Final data:", l_matrix)
        for l_row in range(len(l_matrix)):
            for l_column in range(len(l_matrix[l_row])):
                l_count_islands += l_matrix[l_row][l_column]
        print(f"\nTotal islands: {l_count_islands}\n")
    else:
        print("USAGE:  count_the_islands_ca.py expected-rows expected-columns filename")

    return


#  The usual to keep us out of trouble if someone imports this file
if (__name__ == "__main__"):
    main(g_argv)