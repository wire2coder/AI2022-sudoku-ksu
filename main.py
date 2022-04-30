# Terry Strickland
# Puzzles are from 'sudokuwiki.org'

import numpy as np
import time

# fucntions for generating 'index' for rows, columns, and 'houses'
#################################################

# return all the 'cells' in each column
all_columns = [[(i, j) for j in range(9)] for i in range(9)]

# return all the 'cells' in each row
all_rows = [[(i, j) for i in range(9)] for j in range(9)]

# return all the 'cells' in each 'block 3x3'
all_blocks = [[((i // 3) * 3 + j // 3, (i % 3) * 3 + j % 3)
               for j in range(9)] for i in range(9)]

# all the 'columns' 'rows' and 'squares' are all 'houses'
all_houses = all_columns + all_rows + all_blocks


# extra functions
#################################################
# generates all 'index location' for all 'cells' in a puzzle
def create_all_index(a, b):
    permutations = []
    for j in range(b):
        for i in range(a):
            permutations.append((i, j))
    return permutations


# replacing zeros with 'candidates' [1,2,3,4,5,6,7,8,9]
def insert_candi_into_cells(puzzle):
    sudoku = np.empty((9, 9), dtype=object)
    asdf = create_all_index(9, 9)
    for (j, i) in asdf:
        if puzzle[i, j] != 0:
            sudoku[i][j] = [puzzle[i, j], ]
        else:
            sudoku[i][j] = [i for i in range(1, 10)]
    return sudoku


# find out the number of 'solved cells' in the puzzle
def n_solved(sudoku):
    solved = 0
    for (i, j) in create_all_index(9, 9):
        if len(sudoku[i, j]) == 1:
            solved += 1
    return solved


# find out the number of 'candidates' that needs to be removed
def n_to_remove(sudoku):
    to_remove = 0
    for (i, j) in create_all_index(9, 9):
        to_remove += len(sudoku[i, j]) - 1
    return to_remove


# Print full sudoku, with all candidates (rather messy)
def print_sudoku(sudoku):
    for j in range(9):
        out_string = "|"
        out_string2 = " " * 10 + "|"
        for i in range(9):
            if len(sudoku[i, j]) == 1:
                out_string2 += str(sudoku[i, j][0]) + " "
            else:
                out_string2 += "  "

            for k in range(len(sudoku[i, j])):
                out_string += str(sudoku[i, j][k])

            what1 = len(sudoku[i, j])
            what2 = 10 - what1
            for k in range(10 - len(sudoku[i, j])):
                out_string += " "
            if (i + 1) % 3 == 0:
                out_string += " | "
                out_string2 += "|"

        if (j) % 3 == 0:
            print("-" * 99, " " * 10, "-" * 22)
        print(out_string, out_string2)
    print("-" * 99, " " * 10, "-" * 22)


# functions for solving the puzzle

# 0. Simple Elimination
###################################
def simple_elimination(sudoku):
    elimination_count = 0
    num_round = 0

    for group in all_houses:
        num_round += 1
        for cell in group:
            if len(sudoku[cell]) == 1:
                for cell2 in group:
                    num_to_eli = sudoku[cell][0]
                    current_cell = sudoku[cell2]
                    if num_to_eli in current_cell and cell2 != cell:
                        current_cell.remove(num_to_eli)
                        elimination_count += 1

                        # debug print
                        # print_sudoku(sudoku)
    return elimination_count


# 1. Hidden Single
###################################
def hidden_single(sudoku):

    def find_only_number_in_group():
        nonlocal group
        nonlocal number
        count = 0
        removed = 0
        cell_to_clean = (-1, -1)

        for cell in group:
            current_cell = sudoku[cell]
            for n in current_cell:
                if n == number:
                    count += 1
                    cell_to_clean = cell
        if count == 1 and cell_to_clean != (-1, -1) \
                and len(sudoku[cell_to_clean]) > 1:
            removed = len(sudoku[cell_to_clean]) - 1  # 'subtract 1' because ...
            sudoku[cell_to_clean] = [number]

            # debug print
            # print_sudoku(sudoku)
        return removed

    # logic start here
    removed_items = 0  # total 'item' that got removed
    for number in range(1, 10):
        for group in all_houses:
            asdf1 = find_only_number_in_group()
            removed_items = removed_items + asdf1

    return removed_items


# 3. Brute Force
#####################

# Helper: generate list of all the 'houses' of the current 'cell'
def cellInHouse():
    out = {(-1, -1): []}

    for (i, j) in create_all_index(9, 9):
        out[(i, j)] = []
        for h in all_houses:
            if (i, j) in h:
                out[(i, j)].append(h)
    return out


def next_cell__to_brute_force(sudoku):
    for (i, j) in create_all_index(9, 9):
        if len(sudoku[i, j]) > 1:
            return (i, j)


def brute_force(s, print_output11):
    solution = []
    t = time.time()
    recursive_call_counter = 0

    cellHouse = cellInHouse()

    def is_broken(s, last_cell):
        asdf1 = cellHouse[last_cell]

        for house in asdf1:
            house_data = []
            for cell in house:
                if len(s[cell]) == 1:
                    asdf1 = s[cell][0]
                    house_data.append(asdf1)

            set_house_data_len = len(set(house_data))
            house_data_len = len(house_data)
            if len(house_data) != set_house_data_len:
                return True # when will this condition happens? when '[1,3,4] and [4]' in [list] ... (set)[list]
        return False # default 'return' value

    def iteration(s, last_cell=(-1, -1)):
        nonlocal solution
        nonlocal recursive_call_counter # counting recursive function 'iteration()' gets 'executED'

        recursive_call_counter += 1
        if recursive_call_counter == 338624:
            print(f'debug wait, recursive_call_counter: {recursive_call_counter}')

        if recursive_call_counter % 100000 == 0 and print_output11:
            print("Iteration", recursive_call_counter)

        # is broken - return fail, when you are trying a '4' but you found another SINGLE 4 in the 'house'
        is_broken1 = is_broken(s, last_cell) # len and len('set') have same value, default value 'False'
        if is_broken1:
            return -1 # 'exit point' 'return' -1 to what?? the 'outter most' iteration(), remove 1 'iteration()' from 'stack'

        # is solved - return success
        n_to_remove1 = n_to_remove(s)

        # debug code
        if n_to_remove1 < 7:
            print(f"less than {n_to_remove1} 'n_to_remove' now")

        if n_to_remove1 == 0:
            # print ("Solved")
            solution = s
            return 1 # what happens here? 'return' 1 to what?? the 'outter most' iteration()

        # find next unsolved cell
        next_cell = next_cell__to_brute_force(s)

        # apply all options recursively
        s_next_c = s[next_cell]
        for n in s_next_c: # go to next item in [list], if [last item], 'pop' stack
            scopy = s.copy() # copy current 'sudoku' to a new 'sudoku' name 'scopy'
            scopy[next_cell] = [n] # 'location' < '(1) number'
            result = iteration(scopy, next_cell) # if 'result -1' try another number in s_next_cell [4,6,7,8]
            if result == 1: # what does this line do?
                return # what happens here? 'exit point'

    iteration(s)

    if len(solution) > 0:
        if print_output11:
            print("BruteForce took:", time.time() - t, "seconds, with", recursive_call_counter, "attempts made")
        return solution

    # this is only if puzzle is broken and couldn't be forced
    print("The puzzle appears to be broken")
    return s


# Main Solver
#############
def solve(original_puzzle, print_output11):
    report = [0] * 3 # [0, 0 ,0]

    puzzle = insert_candi_into_cells(original_puzzle)
    solved = n_solved(puzzle)
    to_remove = n_to_remove(puzzle)
    if print_output11:
        print("Initial Sudoku:\nsolved cells", solved, " out of 81.\n'Candidates' to remove:", to_remove,"\n")

    t = time.time()

    # Control how the program 'select' which solver functions
    # default value is boolean 'False'
    all_at_once = False

    while to_remove != 0:  # 'item/number' that needs to be remove
        r_step = 0
        item_eliminated_simple = simple_elimination(puzzle)
        report[0] = report[0] + item_eliminated_simple  # report[0] = report[0] + item_eliminated_simple
        r_step = r_step + item_eliminated_simple  # r_step = r_step + item_eliminated_simple

        if all_at_once or r_step == 0:
            item_elim_hid_sing = hidden_single(puzzle)
            report[1] = report[1] + item_elim_hid_sing
            r_step = r_step + item_elim_hid_sing  # 'r_step' is 0, if hidden_single() didn't 'remove' any item, program will go to csp() function

        # check state
        solved = n_solved(puzzle)
        to_remove = n_to_remove(puzzle)

        # Nothing helped, logic failed
        if r_step == 0:
            break

    # print_sudoku(puzzle)
    if print_output11:
        print("Solved with logic:\nnumber of solved cells", solved, "out of 81.\n'Candidates' to remove:", to_remove,"\n")
        print("Logic part took:", time.time() - t)

    if to_remove > 0:
        for_brute = n_to_remove(puzzle)
        puzzle = brute_force(puzzle, print_output11)
        report[2] += for_brute

    # Report:
    legend = [
        'Simple elimination',
        'Hidden single',
        'BruteForce']
    if print_output11:
        print("Used Functions:")
        for i in range(len(legend)):
            print("\t", i, legend[i], ":", report[i])
    return puzzle


# Interface to convert line format to internal format and back
############################################################
def line_from_solution(solution1):
    output = ""
    for item in solution1:
        for item2 in item:
            output += str(item2[0])
    return output


def solve_from_line(line, print_output1=False):
    s_str = ""
    raw_s = line[0:81]
    for ch in raw_s:
        s_str += ch + " "
    s_np1 = np.fromstring(s_str, dtype=int, count=-1, sep=' ')
    s_np = np.reshape(s_np1, (9, 9))

    solved_sudo = solve(s_np, print_output1)
    return line_from_solution(solved_sudo)


# Main function
# program starts here
#################################
if __name__ == "__main__":

    print("Start Program")

    sudokus = [
        ("easy puzzle",
         '000000000000003085001020000000507000004000100090000000500000073002010000000040009'
         ),
        ("medium puzzle",
         '100070009008096300050000020010000000940060072000000040030000080004720100200050003'
         ),
         ("tough puzzle", '309000400200709000087000000750060230600904008028050041000000590000106007006000104'
         ),
         ("escargot puzzle", '100007090030020008009600500005300900010080002600004000300000010041000007007000300'
         ),
         ("Arto Inkala", '800000000003600000070090200050007000000045700000100030001000068008500010090000400'
         )
    ]

    for name_of_puzzle1, sudoku1 in sudokus:
        print('*' * 90)
        print(name_of_puzzle1)
        print(sudoku1)
        print('*' * 90)

        solution = solve_from_line(sudoku1, print_output1=True)
        print('*' * 90)
        print("solution: " + solution)
        print('*' * 90)
        print("\n")

