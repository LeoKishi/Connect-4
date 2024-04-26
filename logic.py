from random import randint
from copy import deepcopy


class Logic:
    def __init__(self):
        self.turn = randint(1,2)
        self.move_count = 0
        self.is_paused = False
        self.can_reset = False
        self.search = Search()

        # 2D list to hold information about each slot
        self.array = [[Slot(row, col) for col in range(7)] for row in range(6)]


    def reset(self):
        self.turn = randint(1,2)
        self.move_count = 0
        self.array = [[Slot(row, col) for col in range(7)] for row in range(6)]


    def update_slot(self, pos: tuple[int, int]):
        '''Assigns a player to the slot at the specified position.'''
        x, y = pos[0], pos[1]
        self.array[x][y].player = self.turn


    def find_bottom(self, pos: tuple[int, int]) -> tuple[int, int] | bool:
        '''Returns the coordinates of the bottomost slot the piece can fall to.'''
        y = pos[1]
        for row in range(5, -1, -1):
            if self.array[row][y].player == 0:
                return (row, y)
    

    def column_is_full(self, col: int) -> bool:
        '''Returns True if the specified column is full, returns False otherwise.'''
        for row in range(6):
            if self.array[row][col].player == 0:
                return False
        return True


    def next_turn(self) -> bool:
        '''Returns true if the game continues to the next turn, returns false if there are no more valid moves.'''
        self.move_count += 1
        if self.move_count == 42:
            return False

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        return True
        

    def search_winner(self) -> list[tuple[int, int]] | bool:
        '''Searches every row and column for a winner.'''
        if segment := self.search.horizontal_search(self.array, self.turn):
            return segment
        
        elif segment := self.search.vertical_search(self.array, self.turn):
            return segment
        
        elif segment := self.search.diagonal_search(self.array, self.turn):
            return segment
        
        elif segment := self.search.mirrored_diagonal_search(self.array, self.turn):
            return segment
        
        else:
            return False


    def get_occupied_slots(self) -> list[tuple[int, int, int]]:
        '''Returns a list of tuples containing the position of every occupied slot and the player occupying it.'''
        occupied_slots = []

        for row in range(6):
            for col in range(7):
                if self.array[row][col].player != 0:
                    occupied_slots.append((row, col, self.array[row][col].player))

        return occupied_slots


class Slot:
    '''Holds information about a slot in the grid.'''
    def __init__(self, x: int, y: int):
        self.pos = [x,y]
        self.player = 0


class Search:
    segment = []

    def horizontal_search(self, array:list[list[int]], turn:int) -> list[tuple[int, int]] | bool:
        '''Returns the winning segment if the search finds 4 consecutive values horizontally, returns False otherwise.'''
        for row in range(6):
            counter = 0
            self.segment = []
            for col in range(7):
                if array[row][col].player == turn:
                    counter += 1
                    self.segment.append(array[row][col].pos)
                else:
                    counter = 0
                    self.segment = []
                if counter >= 4:
                    return self.segment
        return False


    def vertical_search(self, array:list[list[int]], turn:int, mod:bool = False) -> list[tuple[int, int]] | bool:
        '''Returns the winning segment if the search finds 4 consecutive values vertically, returns False otherwise.'''
        for col in range(7):
            counter = 0
            self.segment = []
            for row in range(6):
                if array[row][col].player == turn:
                    counter += 1
                    self.segment.append(array[row][col].pos)
                else:
                    counter = 0
                    self.segment = []
                if counter >= 4:
                    return self.segment
        return False


    def diagonal_search(self, array:list[list[int]], turn:int) -> list[tuple[int, int]] | bool:
        '''Returns the winning segment if the search finds 4 consecutive values diagonally, returns False otherwise.''' 
        array_copy = deepcopy(array)

        # align diagonals vertically to perform vertical search
        counter = 5
        inv_counter = 0
        for row in array_copy:
            for i in range(counter):
                row.insert(0, 0)
            counter -= 1

            for i in range(inv_counter):
                row.append(0)
            inv_counter += 1

        # vertical search
        for col in range(2, 9):
            counter = 0
            self.segment = []
            for row in range(6):
                if array_copy[row][col] != 0 and array_copy[row][col].player ==  turn:
                    counter += 1
                    self.segment.append(array_copy[row][col].pos)
                else:
                    counter = 0
                    self.segment = []
                if counter >= 4:
                    return self.segment
        return False


    def mirrored_diagonal_search(self, array:list[list[int]], turn:int) -> list[tuple[int, int]] | bool:
        '''Returns the winning segment if the search finds 4 consecutive values diagonally, returns False otherwise.''' 
        array_copy = deepcopy(array)

        # align diagonals vertically to perform vertical search
        counter = 5
        inv_counter = 0
        for row in array_copy:
            for i in range(counter):
                row.append(0)
            counter -= 1

            for i in range(inv_counter):
                row.insert(0, 0)
            inv_counter += 1

        # vertical search
        for col in range(2, 9):
            counter = 0
            self.segment = []
            for row in range(6):
                if array_copy[row][col] != 0 and array_copy[row][col].player ==  turn:
                    counter += 1
                    self.segment.append(array_copy[row][col].pos)
                else:
                    counter = 0
                    self.segment = []
                if counter >= 4:
                    return self.segment
        return False




if __name__ == '__main__':
    



    ...