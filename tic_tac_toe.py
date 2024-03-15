import random
from tabulate import tabulate
from typing import Optional, Tuple, Dict
import numpy as np


class TTTBoard:
    def __init__(self, mark: bool) -> None:
        self.comp_char = mark
        self.hum_char = not mark
        self.layout = np.zeros((3, 3))
        self.available_moves_list = [(x_coord, y_coord) for x_coord in range(3) for y_coord in range(3) if self.layout[x_coord, y_coord] != 0]
        self.current_mark = True
        self.last_move: Tuple[int, int] | None = None

    def reset(self) -> None:
        self.layout = np.zeros((3, 3))
        self.available_moves_list = [(x_coord, y_coord) for x_coord in range(3) for y_coord in range(3) if self.layout[x_coord, y_coord] == 0]
        self.current_mark = True
        self.last_move = None
           
    def check_available_move(self, coords: Tuple[int, int]) -> bool:
        x_coord, y_coord = coords
        if (x_coord not in [0, 1, 2]) or (y_coord not in [0, 1, 2]):
            return False
        if self.layout[x_coord, y_coord] != 0:
            return False
        return True

    def place_move(self, coords: Tuple[int, int], mark: bool) -> None:
        if mark != self.current_mark:
            raise Exception ("Move is not in order")
        x_coord, y_coord = coords      
        if self.check_available_move(coords):
            if mark:
                self.layout[x_coord,y_coord] = 1
            else:
                self.layout[x_coord,y_coord] = -1
            self.available_moves_list = [(x_coord, y_coord) for x_coord in range(3) for y_coord in range(3) if self.layout[x_coord, y_coord] ==0]
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
        for x_coord in range(3): 
            b_layout[x_coord] = {}
            for y_coord in range(3):
                if layout[y_coord, x_coord] == 1.0: 
                    b_layout[x_coord][y_coord] = 'X'
                elif layout[y_coord,x_coord] == -1.0: 
                    b_layout[x_coord][y_coord] = '0'
                else: 
                    b_layout[x_coord][y_coord] = '_'
 
        table_data = [[b_layout[y_coord][x_coord] for y_coord in range(3)] for x_coord in range(3)]
        table_headers: list[str] = []
        table = tabulate(table_data, headers=table_headers, tablefmt='fancy_grid', showindex='never')

        print(table)

def game_initialize(first_move: bool) -> TTTBoard:
    board = TTTBoard(first_move)
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
        x_coord = int(i_index) - 1
    except:
        print('Please enter integer values only')
        return None

    if x_coord not in [0, 1, 2]:
        print('value is out of range 1 to 3, please try again')
        return None

    j_index = input('   input column: ')
    try:
        y_coord = int(j_index) - 1
    except:
        print('Please enter integer values only')
        return None

    if y_coord not in [0, 1, 2]:
        print('Value is out of range 1 to 3, please try again')
        return None
    if (x_coord, y_coord) not in legal_moves:
        print('Your move is not possible -  the cell is occupyied, please try again')
        return None
    return (x_coord, y_coord)
            
def game() -> None: 
    
    first_move = random.choice([False, True]) # False - human moves first, True - computer moves first

    board = game_initialize(first_move)
    legal_moves = board.available_moves_list

    while True:
        mark = board.current_mark

        if mark != first_move:
            move = get_coords_from_human(legal_moves)
            if move is None:
                continue
        else:               
            move = random.choice(legal_moves)
            print(f'My move is - row {move[0]+1}, column {move[1]+1}')
        
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