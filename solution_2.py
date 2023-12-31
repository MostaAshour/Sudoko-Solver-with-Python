import time
import numpy as np
import pandas as pd

from math import floor
import collections


def hotline_to_dict(s):
    grid_dict = {}
    for i in range(81):
        v = int(s[i])
        if v == 0:
            grid_dict[f'{i//9}{i%9}'] = set()
    return grid_dict


def checker_t(hotline, r, c):
    sl = set('123456789')

    sq_r, sq_c = [floor(r/3)*3, floor(c/3)*3]

    row = set(hotline[r*9:r*9+9]) #row
    col = set([hotline[c+i*9] for i in range(9)]) #column
    sqr = set(''.join([hotline[(sq_r+i)*9+sq_c:((sq_r+i)*9+sq_c)+3] for i in range(3)])) #square
    mix = sqr.union(row).union(col)
    mix.discard(0)

    res = sl.difference(mix)
    return res
 
    if len(res) == 1:
        return res.pop()
    else:
        return set(res)
    
def eleminate(hotline, grid_dict):
    keys = grid_dict.copy().keys()
    for key in keys:
        r, c = int(key[0]), int(key[1])
        check = checker_t(hotline, r, c)
        if len(check) == 1:
            hotline = hotline[:r*9+c] + check.pop() + hotline[r*9+c+1:]
            grid_dict.pop(key)
        else:
            grid_dict[f'{r}{c}'] = check
    return hotline, grid_dict


def eliminate_singles(hotline, grid_dict):
    keys = grid_dict.copy().keys()
    for key in keys:
        r, c = int(key[0]), int(key[1])
        if len(grid_dict[key]) == 1:
                hotline = hotline[:r*9+c] + grid_dict[key].pop() + hotline[r*9+c+1:]
                grid_dict.pop(key)
                continue
        
        r, c = int(key[0]), int(key[1])
        check = checker_t(hotline, r, c)
        l = len(grid_dict[key])
        if (l == 0) or (l > len(check)):
            grid_dict[key] = check
    return hotline, grid_dict


def check_twin(grid_dict, cells):
    for i in grid_dict:
        grid_dict[i] = ''.join(grid_dict[i])
    
    count_values = collections.Counter([grid_dict[i] for i in cells])
    for twins, count in count_values.items():
        if 1 < count == len(twins):
            for cell in cells:
                if grid_dict[cell] != twins and set(grid_dict[cell]).intersection(set(twins)):
                    for digit in twins:
                        grid_dict[cell] = grid_dict[cell].replace(digit, '')
    for k in grid_dict:
        grid_dict[k] = set(grid_dict[k])
    return grid_dict

def get_only_possibility(grid_dict, cells):
    values = ''
    for i in cells:
        values += ''.join(grid_dict[i])

    count = collections.Counter(values)
    for val in list(filter(lambda x: count[x]==1, count)):
        for i in cells:
            if val in grid_dict[i]:
                grid_dict[i] = set(val)
    return grid_dict

def implement_naked_twin(grid_dict):
    for r in range(18):
        # we're using the "r//9" to fit rows and columns [0, 1], and "4%9" to move ascending from 0 to 8
        cells = list(filter(lambda x: x[r//9]==str(r%9), grid_dict.keys()))
        grid_dict = check_twin(grid_dict, cells)
        grid_dict = get_only_possibility(grid_dict, cells)

    for i in range(3):
        for j in range(3):  
            # and here the fit for each square
            cells = [f'{i*3+i2}{j*3+j2}' for i2 in range(3) for j2 in range(3)]
            cells = list(filter(lambda x: x in cells, grid_dict.keys()))
            grid_dict = check_twin(grid_dict, cells)
            grid_dict = get_only_possibility(grid_dict, cells)
            
    return grid_dict

def solver_2(grid):
    grid_dict = hotline_to_dict(grid)
    stalled = False
    
    c = 0       
    while True:
        len_before = len(grid_dict.keys())
        grid, grid_dict = eliminate_singles(grid, grid_dict)
        len_after = len(grid_dict.keys())
        len_res = len_before - len_after
        if len_res == 0: 
            c+=1
        else: 
            c=0
        if c == 2:
            grid_dict = implement_naked_twin(grid_dict)
        if len(grid_dict.keys()) == 0:
            break
    return grid

def solve_and_verify_2(data):
    for row in data.iterrows():
        s = solver_2(row[1]["quizzes"]) == row[1]["solutions"]