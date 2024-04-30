import tkinter as tk
from random import choice
from graphics import Graphics
from playsound import playsound
from animation import Sprite
from typing import Callable


class Display(tk.Tk):
    '''
    Initializes the game window.\n
    Arguments:
        mode
            'dark' for dark mode, 'light' for light mode\n
            Light mode by default
    '''
    def __init__(self, theme: str = 'light'):
        super().__init__()

        self.minsize(875, 850)
        self.title('Connect 4')

        if theme == 'dark':
            self.configure(bg= '#201e23')
        elif theme == 'light':
            self.configure(bg= 'white')

        # 2D list with the image labels of each slot
        self.slots = [[col for col in range(7)] for row in range(6)]

        self.mouse_pos = None

        self.graphics = Graphics(self, theme)

        self._create_frames(theme)
        self._create_layout()

    # layout
    def _create_frames(self, theme: str):
        '''Creates frames and set image files.'''
        self.main_frame = tk.Frame(self)

        self.top_wall_frame = Wall(self.main_frame, self.graphics.top_wall)
        self.center_frame = tk.Frame(self.main_frame)

        self.left_wall_frame = Wall(self.center_frame, self.graphics.left_wall).pack(side=tk.LEFT)
        self.grid = Grid(self, self.center_frame, self.graphics.empty_slot, self.slots).pack(side=tk.LEFT)
        self.right_wall_frame = Wall(self.center_frame, self.graphics.right_wall).pack(side=tk.LEFT)

        self.bottom_wall_frame = Wall(self.main_frame, self.graphics.bottom_wall)

        if theme == 'dark':
            bg, fg = '#201e23', 'white'

        elif theme == 'light':
            bg, fg = 'white', '#201e23'

        self.top_frame = TextLabel(self.main_frame, bg=bg, fg=fg)
        self._create_piece_view()


    def _create_layout(self):
        '''Places the frames in the screen.'''
        self.main_frame.pack(fill='none', expand=True)

        self.piece_view.pack(side=tk.TOP, fill='none', expand=False)
        self.top_frame.pack(side=tk.TOP, fill='both', expand=True)
        self.top_frame.pack_propagate(0)
        
        self.bottom_wall_frame.pack(side=tk.BOTTOM)
        self.center_frame.pack(side=tk.BOTTOM)
        self.top_wall_frame.pack(side=tk.BOTTOM)

        self.hide_play_again()


    def _create_piece_view(self):
        '''Creates the frame for the piece indicator.'''
        self.columns = [None for col in range(7)]
        self.piece_view = PieceView(self, self.main_frame, self.graphics.empty_space, self.columns)

        ImgLabel(self.piece_view, image=self.graphics.empty_space_edge).grid(row=0, column=0)
        ImgLabel(self.piece_view, image=self.graphics.empty_space_edge).grid(row=0, column=8)

    # gameover text
    def show_play_again(self, winner: str):
        '''Show the play again text.'''
        if winner == 0:
            self.top_frame.winner['text'] = 'Tie!'

        if winner == 1:
            self.top_frame.winner['text'] = 'Red wins!'
        elif winner == 2:
            self.top_frame.winner['text'] = 'Orange wins!'

        self.piece_view.pack_forget()
        self.top_frame.pack(side=tk.TOP, fill='both', expand=True)
        self.top_frame.pack_propagate(0)


    def hide_play_again(self):
        '''Hides the play again text.'''
        self.top_frame.pack_forget()
        self.piece_view.pack(side=tk.TOP, fill='none', expand=False)

    # player input binding
    def bind_click_event(self, action):
        '''
        Binds a mouse click event to each slot.\n
        The event calls the action function and passes in the coordinates of the clicked slot.
        '''
        for row in range(6):
            for col in range(7):
                self.slots[row][col].bind('<Button-1>', lambda event, x=row, y=col: action(x,y))


    def bind_hover_event(self, show, hide):
        '''
        Binds a hover event fo every slot.\n
        When the mouse hovers over the slot the show function is called.\n
        When the mouse stops hovering over the slot the hide function is called.
        '''
        for row in range(6):
            for col in range(7):
                self.slots[row][col].bind('<Enter>', lambda event, col=col: show(col))
                self.slots[row][col].bind('<Leave>', lambda event, col=col: hide(col))


    def bind_spacebar_event(self, reset):
        '''Binds a spacebar key press event.'''
        self.bind('<Key>', lambda event: reset(True if event.keysym == 'space' else False))

    # animations
    def fall_animation(self, board_state:list['str'], next_board_state:Callable):
        '''Plays the falling animation for every occupied slot.'''
        for _ in range(7):
            for row in range(6):
                for col in range(7):
                    if board_state[row][col] == '':
                        self.slots[row][col].set_image(self.graphics.empty_slot)
                    elif _ == 0:
                        self.slots[row][col].chain(self.graphics.fall_start[board_state[row][col]], fps=15)
                    else:
                        self.slots[row][col].chain(self.graphics.fall[board_state[row][col]], fps=15)
            next_board_state()

        for row in range(6):
            for col in range(7):
                self.slots[row][col].chain_image(self.graphics.empty_slot, timer=1)
                self.slots[row][col].play()


    def winner_animation(self, winner_segment:list[tuple[int, int]], turn: int):
        '''Executes the animation for the winning segment.'''
        if turn == 1:
            smoke = self.graphics.red_smoke
            crown = self.graphics.red_crown

        elif turn == 2:
            smoke = self.graphics.orange_smoke
            crown = self.graphics.orange_crown

        playsound('assets/sound/crown.wav', block=False)

        for pos in winner_segment:
            x, y = pos[0], pos[1]

            self.slots[x][y].play(smoke, loop=False, fps=12)
            self.slots[x][y].chain(crown, loop=True, fps=6)


    def draw_indicator(self, turn: int, column_is_full: Callable):
        '''Starts the indicator animation.'''
        self.erase_indicator(column_is_full)

        if turn == 1:
            indicator = self.graphics.red_indicator
            indicator_bottom = self.graphics.red_indicator_bottom

        elif turn == 2:
            indicator = self.graphics.orange_indicator
            indicator_bottom = self.graphics.orange_indicator_bottom

        if column_is_full(self.mouse_pos):
            self.columns[self.mouse_pos].set_image(self.graphics.empty_space)
        else:
            self.columns[self.mouse_pos].play(indicator, loop=True)
            self.slots[0][self.mouse_pos].set_image(indicator_bottom)


    def erase_indicator(self, column_is_full: Callable):
        '''Changes the indicator into an empty image.'''
        for _ in range(7):
            if not column_is_full(_):
                self.slots[0][_].set_image(self.graphics.empty_slot)
            self.columns[_].set_image(self.graphics.empty_space)


    def drop_animation(self, pos:tuple[int, int], sequence:list[tk.PhotoImage], sequence_bot:list[tk.PhotoImage], image:tk.PhotoImage, func):
        x, y = pos[0], pos[1]

        column = [0 for _ in range(pos[0]+1)]
        column[0] = 1
        if len(column) > 1:
            column[1] = 2

        for _ in range(pos[0]+1):
            for row in range(pos[0]+1):
                if column[row] == 1 and row < pos[0]:
                    self.slots[row][y].chain(sequence, timer=10, fps=30)
                if column[row] == 2:
                    self.slots[row][y].chain(sequence_bot, timer=10, fps=30)
                if column[row] == 0:
                    self.slots[row][y].chain_image(self.graphics.empty_slot, timer=10)
                
            column.pop()
            column.insert(0, 0)

        self.slots[pos[0]][y].chain_image(image, timer=1)
        self.slots[pos[0]][y].chain_func(func)

        for row in range(pos[0]+1):
            self.slots[row][y].play()

    # player interaction
    def fill_slot(self, pos: tuple[int, int], turn: int, func:Callable):
        '''Places a piece of the specified color at the specified position.'''
        x, y = pos[0], pos[1]

        if turn == 1:
            sequence = self.graphics.r_fall_top
            sequence_bot = self.graphics.r_fall_bot
            image = self.graphics.red_slot

        elif turn == 2:
            sequence = self.graphics.o_fall_top
            sequence_bot = self.graphics.o_fall_bot
            image = self.graphics.orange_slot

        sounds = ['assets/sound/click1.wav',
                  'assets/sound/click2.wav',
                  'assets/sound/click3.wav']

        playsound(choice(sounds), block=False)
        self.drop_animation(pos, sequence, sequence_bot, image, func)


    def reset(self):
        '''Resets the slots image.'''
        for row in range(6):
            for col in range(7):
                self.slots[row][col].set_image(self.graphics.empty_slot)




class ImgLabel(tk.Label):
    '''Creates a pre-configured label to remove boilerplate code by passing in default values.'''
    def __init__(self, parent, image):
        super().__init__(parent,
                         image=image,
                         relief=tk.FLAT,
                         borderwidth=0,
                         highlightthickness=0)


class Grid(tk.Frame):
    '''Creates a frame and places a grid of image labels inside of it.'''
    def __init__(self, display, parent, image, slots: list[list[int]]):
        super().__init__(parent)

        for row in range(6):
            for col in range(7):
                slots[row][col] = Sprite(display, self, image)
                slots[row][col].grid(row=row, column=col)


class Wall(tk.Frame):
    '''Creates a frame and places an image inside of it.'''
    def __init__(self, parent, image):
        super().__init__(parent)

        ImgLabel(self, image).pack()


class PieceView(tk.Frame):
    '''Creates a frame and places a grid of image labels inside of it.'''
    def __init__(self, display, parent, image, columns: list[list[int]]):
        super().__init__(parent)

        for col in range(7):
            columns[col] = Sprite(display, self, image)
            columns[col].grid(row=0, column=col+1)


class TextLabel(tk.Frame):
    '''Creates a frame and places labels inside of it.'''
    def __init__(self, parent, bg: str, fg: str):
        super().__init__(parent, height=125, bg=bg)

        self.winner = tk.Label(self, font=('Calibri', 15), bg=bg, fg=fg)

        self.play_again = tk.Label(self, text='Press SPACE to play again',
                                   font=('Calibri', 12), bg=bg, fg=fg)
        
        self.winner.pack(pady=(30,0))
        self.play_again.pack(pady=(30,0))




def main():
    display = Display('light')
    






    display.mainloop()



if __name__ == '__main__':
    main()