import copy

class Check:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    winning_segment = [] # position of the 4 squares that won the game

    def search_winner(self, array, turn):
        if self.horizontal_search(array, turn):
            return True
        if self.vertical_search(array, turn):
            return True
        if self.diagonal_search(array, turn, 'incline'):
            return True
        if self.diagonal_search(array, turn, 'decline'):
            return True


    def horizontal_search(self, array, turn):
        for row in array:
            counter = 0
            for i in row:
                if i.player == turn:
                    counter += 1
                    self.winning_segment.append(i.get_pos())
                else:
                    counter = 0
                    self.winning_segment = []
                if counter >= 4:
                    return True


    def vertical_search(self, array, turn):
        for row in range(self.width):
            counter = 0
            for col in range(self.height):
                if array[col][row].player == turn:
                    counter += 1
                    self.winning_segment.append(array[col][row].get_pos())
                else:
                    counter = 0
                    self.winning_segment = []
                if counter >= 4:
                    return True


    def diagonal_search(self, array, turn, direction):
        # align diagonals vertically to perform vertical search
        array_copy = copy.deepcopy(array)
        counter = (self.height - 1)
        inv_counter = 0
        for row in array_copy:
            for i in range(counter):
                if direction == 'incline':
                    row.append(0)
                elif direction == 'decline':
                    row.insert(0, 0)
            counter -= 1
            for i in range(inv_counter):
                if direction == 'incline':
                    row.insert(0, 0)
                elif direction == 'decline':
                    row.append(0)
            inv_counter += 1
        # vertical search
        for row in range(2, (self.width + 2)): # adjusted range to exclude segments smaller than 4
            counter = 0
            for col in range(self.height):
                if (array_copy[col][row] != 0) and (array_copy[col][row].player == turn):
                    counter += 1
                    self.winning_segment.append(array_copy[col][row].get_pos())
                else:
                    counter = 0
                    self.winning_segment = []
                if counter >= 4:
                    return True
