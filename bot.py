from random import choice


class Bot:
    array = None
    weighted_board = None


    def _set_default(self, game_array:list[list]):
        '''Redefines the lists.'''
        self.array = game_array
        self.weighted_board = [[0 for col in range(7)] for row in range(6)]


    def _get_board_weight(self, player:int):
        '''Adds weight to the slots and registers the weights in the 'weighted_board' attribute.'''
        positions = self._get_piece(player)

        for pos in positions:
            self._directions(pos, player)


    def _get_piece(self, player:int) -> list[tuple[int, int]]:
        '''Returns the position of every piece of the specified player.'''
        pos = []

        for row in range(6):
            for col in range(7):
                if self.array[row][col].player == player:
                    pos.append((row,col))
                    
        return pos


    def _directions(self, pos:tuple[int, int], player:int):
        '''Searches for every direction from the given position.'''
        x, y = pos[0], pos[1]
        self._set_weight([(x-i,y) for i in range(1,4) if self._in_bounds(x-i,y)], player) # up
        self._set_weight([(x,y+i) for i in range(1,4) if self._in_bounds(x,y+i)], player) # right
        self._set_weight([(x,y-i) for i in range(1,4) if self._in_bounds(x,y-i)], player) # left
        self._set_weight([(x-i,y+i) for i in range(1,4) if self._in_bounds(x-i,y+i)], player) # up right
        self._set_weight([(x-i,y-i) for i in range(1,4) if self._in_bounds(x-i,y-i)], player) # up left
        self._set_weight([(x+i,y+i) for i in range(1,4) if self._in_bounds(x+i,y+i)], player) # down right
        self._set_weight([(x+i,y-i) for i in range(1,4) if self._in_bounds(x+i,y-i)], player) # down left


    def _set_weight(self, line:list[tuple[int, int]], player:int):
        '''Registers the weight in the 'weighted_board' attribute.'''
        weighted = list()

        can_complete = self._get_individual_weight(line, weighted, player)

        if not can_complete:
            return
        
        for pos in weighted:
            row, col = pos[0], pos[1]
            weight = pos[2]

            if self.weighted_board[row][col] < weight:
                self.weighted_board[row][col] = weight


    def _get_individual_weight(self, line:list[tuple[int, int]], weighted:list, player:int) -> bool:
        '''Lists the individual slots and their weights. Returns True if a line of 4 pieces can be formed.'''
        if len(line) < 3:
            return

        if player == 1:
            ally, enemy = 1, 2
        elif player == 2:
            ally, enemy = 2, 1

        can_complete = bool
        weight = 0

        for i in range(len(line)):
            row, col = line[i][0], line[i][1]

            if not self._in_bounds(row,col):
                continue

            if self.array[row][col].player == ally:
                weight += 1
                can_complete = True

            elif self.array[row][col].player == enemy:
                if i > 1 and self.array[row][col-(i+2)].player != enemy and self._in_bounds(row, col-(i+2)):
                    continue
                else:
                    return

        for pos in line:
            row, col = pos[0], pos[1]
            if self.array[row][col].player == 0:
                if self._is_floating((row,col)):
                    break
                weighted.append((row, col, weight))

        return can_complete


    def _is_floating(self, pos:tuple[int, int]) -> bool:
        '''Returns True if the given position has no pieces below it, returns False otherwise.'''
        x, y = pos[0], pos[1]
        if (x < 5) and self.array[x+1][y].player == 0:
            return True
        else:
            return False


    def _in_bounds(self, x:int = None, y:int = None) -> bool:
        '''Returns True if the given coordinates are within the grid boundaries, returns False otherwise.'''
        inside = bool

        if not y:
            inside = x >= 0 and x < 6
        elif not x:
            inside = y >= 0 and y < 7
        else:
            inside = (x >=0 and x < 6) and (y >= 0 and y < 7)

        return inside
    

    def make_move(self, game_array:list[list]) -> tuple[int, int]:
        '''Returns the best valid move to play.'''
        self._set_default(game_array)

        self._get_board_weight(2)
        atk_moves = self._get_weighted_pos()
        self._get_board_weight(1)
        def_moves = self._get_weighted_pos()

        strong_atk = atk_moves[1]
        strong_def = def_moves[1]
        weak_atk = atk_moves[0]
        weak_def = def_moves[0]

        move = None

        if strong_atk:
            move = choice(strong_atk)
        elif strong_def:
            move = choice(strong_def)
        elif weak_atk:
            move = choice(weak_atk)
        elif weak_def:
            move = choice(weak_def)
        else:
            move = choice(self._get_incomplete_columns())

        return move


    def _get_weighted_pos(self) -> tuple[list, list]:
        '''Returns the positions of the weighted slots, separated by their respective weights.'''
        weak = list()
        strong = list()

        for row in range(6):
            for col in range(7):
                if self.weighted_board[row][col] == 1:
                    weak.append((row,col))

                elif self.weighted_board[row][col] == 2:
                    strong.append((row,col))

        return (weak, strong)


    def _get_incomplete_columns(self) -> list[tuple]:
        '''Returns the positions of incomplete columns.'''
        columns = []

        for col in range(7):
            if self.array[0][col].player == 0:
                columns.append((0, col))

        return columns




if __name__ == '__main__':


    ...