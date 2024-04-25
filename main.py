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
            search_and_continue(row,col)


def show_indicator(col: int):
    '''Shows the piece indicator image on top of the column.'''
    if not game.is_paused:
        if game.turn == 1:
            top_sequence = display.red_indicator
            bottom_image = display.red_indicator_bottom

        elif game.turn == 2:
            top_sequence = display.orange_indicator
            bottom_image = display.orange_indicator_bottom

        if game.collumn_is_full(col):
            display.columns[col]['image'] = display.empty_space
        else:
            display.start_animation(display.columns[col], top_sequence, loop=True)
            display.slots[0][col]['image'] = bottom_image


def hide_indicator(col: int):
    '''Removes the piece indicator image from the column.'''
    if not game.is_paused:
        if not game.collumn_is_full(col):
            display.slots[0][col]['image'] = display.empty_slot
        display.stop_animation() 
        display.columns[col]['image'] = display.empty_space


def reset_game(spacebar_pressed: bool):
    '''Plays the reset animation then restarts the game.'''
    if spacebar_pressed and game.can_reset:
        game.can_reset = False

        display.stop_animation()
        display.reset_board(game.array)
        display.hide_play_again()
        display.after(1100, unpause)

        display.reset()
        game.reset()


def winner_found(row:int, col:int, segment:list[list[int,int]]):
    '''Stops the game and shows the winner.'''
    hide_indicator(col)
    display.show_play_again(game.turn)
    display.show_winner(segment, game.turn)
    display.after(1650, enable_reset)
    game.is_paused = True


def search_and_continue(row: int, col: int):
    '''Searches for a winner and starts next turn if none is found.'''
    if segment := game.search_winner():
        winner_found(row, col, segment)
        return
    else:
        if game.next_turn():
            hide_indicator(col)
            show_indicator(col)
        else:
            hide_indicator(col)
            display.show_play_again(0)
            enable_reset()
            game.is_paused = True


def enable_reset():
    game.can_reset = True

def unpause():
    game.is_paused = False


# binding user input
display.bind_click_event(action)
display.bind_hover_event(show=show_indicator, hide=hide_indicator)
display.bind_spacebar_event(reset_game)





if __name__ == '__main__':
    display.mainloop()



    ...




