from gui import Display
from logic import Logic


display = Display(theme='dark')
game = Logic()


def action(row: int, col: int):
    '''Places a piece in the selected column.'''
    def timed_call():
        if not search_and_continue(row,col):
            display.draw_indicator(game.turn, game.column_is_full)
        game.can_click = True

    if not game.is_paused and game.can_click:
        if not game.column_is_full(col):
            pos = game.find_bottom((row, col))

            game.can_click = False
            display.fill_slot(pos, game.turn, timed_call)
            
            game.update_slot(pos)
            

def show_indicator(col: int):
    '''Shows the piece indicator on top of the column.'''
    if not game.is_paused:
        display.mouse_pos = col
        display.draw_indicator(game.turn, game.column_is_full)


def hide_indicator(col: int):
    '''Removes the piece indicator from the column.'''
    if not game.is_paused:
        display.erase_indicator(game.column_is_full)


def reset_game(spacebar_pressed: bool):
    '''Plays the reset animation then restarts the game.'''
    if spacebar_pressed and game.can_reset:
        game.can_reset = False

        display.hide_play_again()
        display.fall_animation(game.get_board_state(), game.next_board_state)

        height = game.get_tallest_collumn()
        delay = 1100

        if height == 5:
            delay += 200
        elif height == 6:
            delay += 400

        display.after(delay, restart)


def winner_found(row:int, col:int, segment:list[list[int,int]]):
    '''Stops the game and shows the winner.'''
    game.is_paused = True

    display.winner_animation(segment, game.turn)
    display.after(800, enable_reset)
    

def search_and_continue(row: int, col: int):
    '''Searches for a winner and starts next turn if none is found.'''
    
    if segment := game.search_winner():
        hide_indicator(col)
        winner_found(row, col, segment)
        return True
    else:
        if not game.next_turn():
            enable_reset(tie=True)
            game.is_paused = True
        return False


def enable_reset(tie:bool = False):
    if tie:
        display.show_play_again(0)
    else:
        display.show_play_again(game.turn)
    game.can_reset = True


def restart():
    display.reset()
    game.reset()
    game.is_paused = False
    game.can_click = True
    

# binding user input
display.bind_click_event(action)
display.bind_hover_event(show_indicator, hide_indicator)
display.bind_spacebar_event(reset_game)




if __name__ == '__main__':
    display.mainloop()



    ...




