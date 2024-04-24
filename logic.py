from random import randint
from copy import deepcopy


class Logic:
    def __init__(self):
        self.turn = randint(1,2)
        self.is_paused = False
        self.color = {1:'Red', 2:'Orange'}
        self.search = Search()

        # 2D list to hold information about each slot
        self.array = [[0 for col in range(7)] for row in range(6)]


    def reset(self):
        self.turn = randint(1,2)
        self.is_paused = False
        self.create_slots()


    def update_slot(self, pos: tuple[int, int]):
        '''Assigns a player to the slot at the specified position.'''
        x, y = pos[0], pos[1]
        self.array[x][y] = self.turn


    def find_bottom(self, pos: tuple[int, int]) -> tuple[int, int] | bool:
        '''Returns the coordinates of the bottomost slot the piece can fall to.'''
        y = pos[1]
        for row in range(5, -1, -1):
            if self.array[row][y] == 0:
                return (row, y)
    

    def collumn_is_full(self, col: int) -> bool:
        '''Returns True if the specified column is full, returns False otherwise.'''
        for row in range(6):
            if self.array[row][col] == 0:
                return False
        return True


    def next_turn(self):
        '''Alternate between players.'''
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1


    def search_winner(self):
        '''Searches every row and column for a winner.'''
        if segment := self.search.horizontal_search(self.array, self.turn):
            return True
        elif segment := self.search.vertical_search(self.array, self.turn):
            return True
        elif segment := self.search.diagonal_search(self.array, self.turn):
            return True
        elif segment := self.search.mirrored_diagonal_search(self.array, self.turn):
            return True
        else:
            return False


class Search:
    segment = []

    def horizontal_search(self, array:list[list[int]], turn:int) -> list[tuple[int, int]] | bool:
        '''Returns the winning segment if the search finds 4 consecutive values horizontally, returns False otherwise.'''
        for row in range(6):
            counter = 0
            for col in range(7):
                if array[row][col] == turn:
                    counter += 1
                    self.segment.append((row,col))
                else:
                    counter = 0
                    self.segment = []
                if counter >= 4:
                    return self.segment
        return False


    def vertical_search(self, array:list[list[int]], turn:int, mod:bool = False) -> list[tuple[int, int]] | bool:
        '''Returns the winning segment if the search finds 4 consecutive values vertically, returns False otherwise.'''
        if mod:
            range_val = range(2, 9)
        else:
            range_val = range(7)

        for col in range_val:
            counter = 0
            for row in range(6):
                if array[row][col] == turn:
                    counter += 1
                    self.segment.append((row, col))
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
        return self.vertical_search(array_copy, turn, mod=True)


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
        return self.vertical_search(array_copy, turn, mod=True)




if __name__ == '__main__':
    



    ...