from gui import Display
from logic import Logic


display = Display(theme='dark')
game = Logic()


def action(row: int, col: int):
    '''Places a piece in the selected column.'''
    if not game.is_paused:
        if not game.collumn_is_full(col):
            pos = game.find_bottom((row, col))
            display.fill_slot(pos, game.turn)
            game.update_slot(pos)
            search_and_continue(col)


def show_indicator(col: int):
    '''Shows the piece indicator image on top of the column.'''
    if not game.is_paused:
        if game.turn == 1:
            image = display.red_slot
        elif game.turn == 2:
            image = display.orange_slot

        if game.collumn_is_full(col):
            display.columns[col]['image'] = display.empty_space
        else:
            display.columns[col]['image'] = image


def hide_indicator(col: int):
    '''Removes the piece indicator image from the column.'''
    display.columns[col]['image'] = display.empty_space


# binding user input
display.bind_click_event(action)
display.bind_hover_event(show=show_indicator, hide=hide_indicator)


def search_and_continue(col: int):
    '''Searches for a winner, start next turn if none is found.'''
    if game.search_winner():
        print(f'{game.color[game.turn]} wins!')
        hide_indicator(col)
        game.is_paused = True
        return
    else:
        game.next_turn()
        show_indicator(col)







if __name__ == '__main__':
    display.mainloop()



    ...




