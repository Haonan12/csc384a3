# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the warehouse domain.

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def binary_not_eql_cons(solved_board, row1, col1, row2, col2):
    var1 = solved_board[row1][col1]
    var2 = solved_board[row2][col2]

    tuple_list = [(a, b) for a in var1.cur_domain() for b in var2.cur_domain() if a != b]
    con = Constraint("row1{}col1{}row2{}col2{}".format(row1, col1, row2, col2), [var1, var2])
    con.add_satisfying_tuples(tuple_list)
    return con

def sum_col_cons(solved_board, cols_sum, col):
    scope = [row[col] for row in solved_board]
    domains = [row[col].cur_domain() for row in solved_board]

    tuple_list = [comb for comb in itertools.product(*domains) if sum(comb) == cols_sum[col]]
    con = Constraint("col{}".format(col), scope)
    con.add_satisfying_tuples(tuple_list)
    return con

def diff_row_cons(solved_board, row):
    scope = solved_board[row]
    domains = [var.cur_domain() for var in solved_board[row]]

    tuple_list = [comb for comb in itertools.product(*domains) if len(set(comb)) == len(comb)]
    con = Constraint("row{}".format(row), scope)
    con.add_satisfying_tuples(tuple_list)
    return con

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''

    # IMPLEMENT

    solved_board = [row[:] for row in initial_tenner_board[0]]
    model = CSP("model_1")
    for i in range(len(solved_board)):
        for j in range(10):
            solved_board[i][j] = Variable("row{}col{}".format(i, j),
                                          [solved_board[i][j]] if solved_board[i][j] != -1 else list(range(10)))
            model.add_var(solved_board[i][j])
    for i in range(len(solved_board)):
        for j in range(10):
            if i != 0:
                model.add_constraint(binary_not_eql_cons(solved_board, i, j, i - 1, j))
                if j != 0:
                    model.add_constraint(binary_not_eql_cons(solved_board, i, j, i - 1, j - 1))
                if j != 9:
                    model.add_constraint(binary_not_eql_cons(solved_board, i, j, i - 1, j + 1))
            for k in range(j):
                model.add_constraint(binary_not_eql_cons(solved_board, i, j, i, k))
    for j in range(10):
        model.add_constraint(sum_col_cons(solved_board, initial_tenner_board[1], j))

    return model, solved_board

##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''
    # IMPLEMENT

    solved_board = [row[:] for row in initial_tenner_board[0]]
    model = CSP("model_2")
    for i in range(len(solved_board)):
        for j in range(10):
            solved_board[i][j] = Variable("row{}col{}".format(i, j),
                                          [solved_board[i][j]] if solved_board[i][j] != -1 else list(range(10)))
            model.add_var(solved_board[i][j])
    for i in range(len(solved_board)):
        for j in range(10):
            if i != 0:
                model.add_constraint(binary_not_eql_cons(solved_board, i, j, i - 1, j))
                if j != 0:
                    model.add_constraint(binary_not_eql_cons(solved_board, i, j, i - 1, j - 1))
                if j != 9:
                    model.add_constraint(binary_not_eql_cons(solved_board, i, j, i - 1, j + 1))
        model.add_constraint(diff_row_cons(solved_board, i))
    for j in range(10):
        model.add_constraint(sum_col_cons(solved_board, initial_tenner_board[1], j))

    return model, solved_board
