import random
from tabulate import tabulate
from typing import Optional, Tuple, Dict
import numpy as np
import pandas as pd

class ttt_board:
    def __init__(self, mark: bool) -> None:
        self.comp_char = mark
        self.hum_char = not mark
        self.layout = np.zeros((3, 3))
        self.available_moves_list = [(i, j) for i in range(3) for j in range(3) if self.layout[i, j] != 0]
        self.current_mark = True
        self.last_move: Tuple[int, int] | None = None

    def reset(self) -> None:
        self.layout = np.zeros((3, 3))
        self.available_moves_list = [(i, j) for i in range(3) for j in range(3) if self.layout[i,j] == 0]
        self.current_mark = True
        self.last_move = None
           
    def check_available_move(self, coords: Tuple[int, int]) -> bool:
        i, j = coords
        if (i not in [0, 1, 2]) or (j not in [0, 1, 2]):
            return False
        if self.layout[i, j] != 0:
            return False
        return True

    def place_move(self, coords: Tuple[int, int], mark: bool) -> None:
        if mark != self.current_mark:
            raise Exception ("Move is not in order")
        i, j = coords      
        if self.check_available_move(coords):
            if mark:
                self.layout[i,j] = 1
            else:
                self.layout[i,j] = -1
            self.available_moves_list = [(i, j) for i in range(3) for j in range(3) if self.layout[i,j] ==0]
            self.current_mark = not self.current_mark
            self.last_move = coords

    def check_for_win(self, mark: bool) -> bool:
        layout = self.layout
        if self.last_move is None:
            return False
        sign = 1 if mark else -1
        
        if layout[0,0] + layout[1,1] + layout[2,2] == 3 * sign:
            return True
        if layout[2,0] + layout[1,1] + layout[0,2] == 3 * sign:
            return True
        for i in range(3):    
            if layout[i,0] + layout[i,1] + layout[i,2] == 3 * sign:
                return True
            if layout[0,i] + layout[1,i] + layout[2,i] == 3 * sign:
                return True
        return False

    def print_board(self) -> None:
        layout = self.layout
        b_layout: Dict[int, Dict[int, str]] = {}
        for i in range(3): 
            b_layout[i] = {}
            for j in range(3):
                if layout[j,i] == 1.0: 
                    b_layout[i][j] = 'X'
                elif layout[j,i] == -1.0: 
                    b_layout[i][j] = '0'
                else: 
                    b_layout[i][j] = '_'
 
        table_data = pd.DataFrame(b_layout).values.tolist()
        table_headers: list[str] = []
        table = tabulate(table_data, headers=table_headers, tablefmt='fancy_grid', showindex='never')

        print(table)

def game_initialize(first_move) -> ttt_board:
    board = ttt_board(first_move)
    board.reset()



    if first_move:
        print('Computer moves first! My moves are shown as "X" and yours as "0"' )
    else:
        print('Human moves first! Your moves are shown as "X" and mine as "0"')    
    return board

def get_coords_from_human(legal_moves) -> Tuple[int, int] | None:
    print('Your turn, please enter integer from 1 to 3 for row or column')
    i_index = input('   input row: ')
    try:
        i = int(i_index) - 1
    except:
        print('Please enter integer values only')
        return None

    if i not in [0, 1, 2]:
        print('value is out of range 1 to 3, please try again')
        return None

    j_index = input('   input column: ')
    try:
        j = int(j_index) - 1
    except:
        print('Please enter integer values only')
        return None

    if j not in [0, 1, 2]:
        print('Value is out of range 1 to 3, please try again')
        return None
    if (i, j) not in legal_moves:
        print('Your move is not possible -  the cell is occupyied, pleasetry again')
        return None
    return (i, j)
            
def game() -> None: 
    
    first_move = random.choice([False, True]) # False - human moves first, True - computer moves first

    board = game_initialize(first_move)
    legal_moves = board.available_moves_list

    while True:
        mark = board.current_mark

        if mark == first_move:
            move = random.choice(legal_moves)
            print(f'My move is - row {move[0]+1}, column {move[1]+1}')
        else:               
            move = get_coords_from_human(legal_moves)
            if move is None:
                continue
        
        board.place_move(move, mark)
        board.print_board()
        
        if board.check_for_win(mark):
            if board.comp_char == mark:
                print("Game over. Human loses!")
                break
            else:
                print('Game over. Human wins!')
                break
        
        legal_moves = board.available_moves_list
        if not legal_moves:
            print('Game over. Draw!')
            break

def main() -> None:
    print('Welcome to tic tac toe console game!')
    print('Once requested, please enter coordinates for your move.')
    while True:
        game()
        if input('Do you want to play again? (y/n)') != 'y':
            break

main()