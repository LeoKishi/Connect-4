from gui import Display
from logic import Logic
from bot import Bot


display = Display(theme='dark')
game = Logic()
bot = Bot()


def action(row: int, col: int, bot_action:bool = False):
    '''Places a piece in the selected column.'''
    if not game.is_paused and (game.can_click or bot_action):
        if game.column_is_full(col):
            return
        
        pos = game.find_bottom((row, col))
        game.can_click = False
        game.update_slot(pos)

        def timed_call():
            if not search_and_continue(row, col):
                display.draw_indicator(game.turn, game.column_is_full)
            if bot_action:
                game.can_click = True

        display.fill_slot(pos, game.turn, timed_call)

        if game.turn == 1 and game.bot_is_enabled:
            display.after(400, bot_move)
        
        


def bot_move():
    pos = bot.make_move(game.array)
    action(pos[0], pos[1], bot_action=True)


def show_indicator(col: int):
    '''Shows the piece indicator on top of the column.'''
    if not game.is_paused:
        display.mouse_pos = col
        display.draw_indicator(game.turn, game.column_is_full)


def hide_indicator():
    '''Removes the piece indicator from the column.'''
    if not game.is_paused:
        display.erase_indicator(game.column_is_full)


def reset_game(spacebar_pressed: bool):
    '''Plays the reset animation then restarts the game.'''
    if spacebar_pressed and game.can_reset:
        game.can_reset = False

        display.hide_endscreen()
        display.fall_animation(game.get_board_state(), game.next_board_state)

        height = game.get_tallest_collumn()
        delay = 1100

        if height == 5:
            delay += 200
        elif height == 6:
            delay += 400

        display.after(delay, restart)


def winner_found(segment:list[list[int,int]]):
    '''Stops the game and shows the winner.'''
    game.is_paused = True

    if game.turn == 1:
        game.red_score += 1
        display.top_frame.add_score(game.turn, game.red_score)
    elif game.turn == 2:
        game.orange_score += 1
        display.top_frame.add_score(game.turn, game.orange_score)

    display.winner_animation(segment, game.turn)
    display.after(800, enable_reset)
    

def search_and_continue(row: int, col: int):
    '''Searches for a winner and starts next turn if none is found.'''
    if segment := game.search_winner(row, col):
        hide_indicator()
        winner_found(segment)
        return True
    else:
        if not game.next_turn():
            enable_reset(tie=True)
            game.is_paused = True
            return True
        return False


def enable_reset(tie:bool = False):
    '''Allows the player to restart the game.'''
    if tie:
        display.show_endscreen(0)
    else:
        display.show_endscreen(game.turn)
    game.can_reset = True


def restart():
    '''Restarts the game.'''
    display.reset()
    game.reset()
    game.is_paused = False

    if game.turn == 1:
        game.can_click = True
    else:
        bot_move()


    

# binding user input
display.bind_click_event(action)
display.bind_hover_event(show_indicator, hide_indicator)
display.bind_spacebar_event(reset_game)




if __name__ == '__main__':
    display.mainloop()
    
    ...