from time import sleep
from IPython.display import display, clear_output

n_moves = 0

def print_grid(a, row, col):
    
    for i in range(9):
        for j in range(9):
            if (i == row) and (j == col):
                print(f"\x1b[34m{a[i][j]}\x1b[0m",end = " ")
            else:
                print(a[i][j],end = " ")
            if j in [2, 5]:
                print('| ', end='')
        if i in [2, 5]:
            print('\n'+'-'*21)
        else:
            print('')
            
def checker(grid, row, col, num):
    '''
    The function checks if this number exists in its row, column or square.
    '''
    
    # Check if this num is in the row
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # Check if this num is in the column
    for x in range(9):
        if grid[x][col] == num:
            return False
 
    # Check if this num is in its 3x3 square 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True

def solver_1(grid, row, col, version, speed=0):
    global n_moves
    
    # check if we are in the last cell in the suduko "last row and column"
    if (row == 8 and col == 8):
        return True
    
    # check if we are in the last cell in the column "but not in the last row"
    if col == 9:
        row += 1
        col = 0
        
    # check if the cell is not 0
    if grid[row][col] > 0:
        return solver_1(grid, row, col + 1, version=version, speed=speed)
    
    # if the cell equals 0
    for num in range(1, 10, 1):
        if checker(grid, row, col, num):
            grid[row][col] = num
            
            # print
            if version == 'slow':
                clear_output(wait=True)
                print('Slow Motion Version:\n')
                print_grid(grid, row, col)
                sleep(speed)
            n_moves += 1
            
            if solver_1(grid, row, col + 1, version=version, speed=speed):
                return True
        grid[row][col] = 0
    return False

def solve_and_verify_1(data):
    for suduko in data:
        s = solver_1(suduko, 0, 0, version='fast')