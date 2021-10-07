############################################################
# CIS 521: Homework 2
############################################################

student_name = "Jingyi Lu"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
import queue


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    # nCr = n!/r!(n-r)!, here is n*n choose n
    result = math.factorial(n*n)/(math.factorial(n)*math.factorial(n*n-n))
    return result
    
def num_placements_one_per_row(n):
    #In n row, for each row, queen has n places
    return (n**n)

def n_queens_valid(board):
    result = True
    #not same col
    if(len(board) != len(set(board))): result = False
    #not same diagonal:
    for i in range(len(board)):
       for j in range(i+1,len(board)):
           if (j-i) == abs(board[j] - board[i]):
               result = False
    return result

def n_queens_helper(n, board):
    #return a list of valid frontiers
    #cannt be same col as those in board
    setDiff = set([x for x in range(n)]) - set(board) 
    lis = []
    for elem in setDiff:
        a = board[:]
        a.append(elem)
        if(n_queens_valid(a)): 
            lis.append(elem)
    return lis

def search(n, depth, current_list, solution):
    if depth == n: 
        #get one valid solution here
        solution.append(current_list)
        return
    
    board = current_list[:]
    possible_next_step = n_queens_helper(n, board)
     #check is possible_next_step is empty， if empty: cannot go on, means dead-end
    if possible_next_step: #not empty
        for step in possible_next_step:
            #add step to current_list
            current_list.append(step)
            #recursion
            search(n, depth+1, current_list, solution)
            current_list = board[:]

def n_queens_solutions(n):
    initial_list = [x for x in range(n)]
    #create an empty list to store solutions
    sol = []
    depth = 1
    for branch in initial_list:
        search(n, depth, [branch], sol)
    return sol

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        #toggle [row,col] 
        if self.board[row][col]:  self.board[row][col] = False
        else: self.board[row][col] = True
        
        #toggle neighbors
        #left
        if(col != 0): 
            if self.board[row][col-1]: self.board[row][col-1] = False
            else: self.board[row][col-1] = True
        #right
        ncol = len(self.board[0])
        nrow = len(self.board)
        if(col != ncol-1): 
            if self.board[row][col+1]: self.board[row][col+1] = False
            else: self.board[row][col+1] = True
        #above
        if(row != 0): 
            if self.board[row-1][col]: self.board[row-1][col] = False
            else: self.board[row-1][col] = True
        #below
        if(row != nrow - 1): 
            if self.board[row+1][col]:self.board[row+1][col] = False
            else: self.board[row+1][col] = True



    def scramble(self):
        nrow = len(self.board)
        ncol = len(self.board[0])
        for i in range(nrow):
            for j in range(ncol):
                if (random.random() < 0.5): self.perform_move(i, j)

    def is_solved(self):
        result = True;
        #check whether there is True
        for lis in self.board:
            for elem in lis:
                if elem == True: result = False
        return result;

    def copy(self):
        nrow = len(self.board)
        ncol = len(self.board[0])
        newPzl = create_puzzle(nrow, ncol)
        for i in range(nrow):
            for j in range(ncol):
                if (self.board[i][j] != newPzl.board[i][j]): 
                    newPzl.board[i][j] = self.board[i][j]
        return newPzl

    def successors(self):
        nrow = len(self.board)
        ncol = len(self.board[0])
        for i in range(nrow):
            for j in range(ncol):
                move = (i,j)
                board = self.copy()
                board.perform_move(i,j)
                yield(move, board)
       

    def find_solution(self):
        frontier = queue.Queue()
        frontier.put(self)
        start = tuple(map(tuple, self.board))
        visited = {}

        while not frontier.empty():
            current = frontier.get()
            current_board = current.get_board()
            current_board_tuple = tuple(tuple(x) for x in current_board)
            if current.is_solved():
                return []

            for move, new_puzzle in current.successors():
                new_board = new_puzzle.get_board()
                new_board_tuple = tuple(tuple(x) for x in new_board)
                if new_board_tuple not in visited:
                    if new_puzzle.is_solved():
                        visited[new_board_tuple] = (current_board_tuple, move)
                        moves = self.backtrack(visited, new_board_tuple)
                        #print(moves, visited)
                        return moves

                    frontier.put(new_puzzle)
                    visited[new_board_tuple] = [current_board_tuple, move]

        return None

    def backtrack(self, visited, goal):
        current = [goal, None]
        start = tuple(map(tuple, self.board))
        path = []
        while current[0] != start:
            current = visited[current[0]]
            path.append(current[1])

        return path

def create_puzzle(rows, cols):
    board = [[False for i in range(cols)] for i in range(rows)]
    newPuzzle = LightsOutPuzzle(board)
    return newPuzzle

############################################################
# Section 3: Linear Disk Movement
############################################################
def getsuccessors(grid):
    for i in range(len(grid)):
        new_grid = grid[:]
        if grid[i] == 0:
            continue
            
        if ((i+1) < len(grid) and grid[i+1] == 0):#right
            new_grid[i+1] = new_grid[i]
            new_grid[i] = 0
            yield ((i, i+1), new_grid)
            
        elif ((i+2) < len(grid) and grid[i+2] == 0 and grid[i+1] != 0): #right 2
            new_grid[i+2] = new_grid[i]
            new_grid[i] = 0
            yield ((i, i+2), new_grid)
            
        elif ((i-1) >= 0 and grid[i-1] == 0): #left
            new_grid[i-1] = new_grid[i]
            new_grid[i] = 0
            yield ((i, i-1), new_grid)
            
        elif ((i-2) >= 0 and grid[i-2] == 0 and grid[i-1] != 0): #left 2
            new_grid[i-2] = new_grid[i]
            new_grid[i] = 0
            yield ((i, i-2), new_grid)


def backtrack(grid, visited, goal, start):
        current = [goal, None] #goal is where we at, current[1] is the move we take from previous to current
        path = []
        while current[0] != start:
            current = visited[tuple(current[0])]
            path.insert(0,current[1])#because we track moves from end to start
        return path

    
def solve_identical_disks(length, n):
    grid = [0 for x in range(length)]
    grid[:n] = [1 for x in range(n)]
    sol = []
    frontier = queue.Queue()
    frontier.put(grid)
    visited = {}
    start1 = grid[:]

    while not frontier.empty():
        current = frontier.get()
        if 1 not in grid[:length-n]: #solved
            return []
        
        for move, new_grid in getsuccessors(current):
            t_new_grid = tuple(new_grid)
            if t_new_grid not in visited:
                if 1 not in new_grid[:(length-n)]: #solved
                    visited[t_new_grid] = (current, move)
                    moves = backtrack(grid, visited, t_new_grid, start = start1)
                    return moves

                frontier.put(new_grid)
                visited[t_new_grid] = [current, move]

    return None


def solve_distinct_disks(length, n):
    grid = [0 for x in range(length)]
    grid[:n] = [x for x in range(1, n+1)]
    sol = []
    frontier = queue.Queue()
    frontier.put(grid)
    visited = {}
    start1 = grid[:]
    final = grid[:]
    final.reverse()
    
    while not frontier.empty():
        current = frontier.get()
        if grid  == final: #solved
            return []
        
        for move, new_grid in getsuccessors(current):
            t_new_grid = tuple(new_grid)
            
            if t_new_grid not in visited:
                if new_grid  == final: #solved
                    visited[t_new_grid] = (current, move)
                    moves = backtrack(grid, visited, t_new_grid, start = start1)
                    return moves

                frontier.put(new_grid)
                visited[t_new_grid] = [current, move]

    return None


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Two days.
"""

feedback_question_2 = """
It's very difficult to implement these algorithms to solve the problems.
"""

feedback_question_3 = """
It seems helpful for us to prepare for job interview questions.
I hope the TAs can explain more about the homeworks during recitation.
"""
