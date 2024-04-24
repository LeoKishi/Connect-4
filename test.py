from gui import Display
from logic import Logic


display = Display('dark')
logic = Logic()


def action(x: int, y: int):
    '''Places a piece in the selected column.'''
    if not logic.is_paused:
        if pos := logic.find_bottom((x,y)):
            display.fill_slot(pos, logic.COLOR[logic.turn])
            logic.assign_player(pos)
            search_and_continue()


display.bind_function(action)


def search_and_continue():
    '''Searches for a winner, start next turn if none is found.'''
    if logic.search_winner():
        print(f'{logic.COLOR[logic.turn]} wins!')
        logic.is_paused = True
        return
    else:
        logic.next_turn()








if __name__ == '__main__':
    display.mainloop()



    ...




