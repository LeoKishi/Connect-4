import tkinter as tk
from tkinter import ttk
from random import randint


class Display(tk.Tk):
    '''
    Initializes the game window.\n
    Arguments:
        mode
            'dark' for dark mode. Light mode by default
    '''
    def __init__(self, theme: str = 'light'):
        super().__init__()

        self.minsize(875, 850)
        self.title('Connect 4')

        # 2D list with the image labels of each slot
        self.slots = [[col for col in range(7)] for row in range(6)]

        # list to hold after functions identifiers
        self.stop_ids = []

        self.load_images(theme)
        self.load_image_sequences(theme)
        self.create_frames()
        self.create_layout()


    def load_images(self, theme: str):
        '''Creates instances of image files.'''
        if theme == 'dark':
            folder = 'dark_theme'
            self.configure(bg= '#201e23')

        elif theme == 'light':
            folder = 'light_theme'
            self.configure(bg= 'white')

        self.top_wall = tk.PhotoImage(file=f'assets/{folder}/top_wall.png')
        self.left_wall = tk.PhotoImage(file=f'assets/{folder}/left_wall.png')
        self.right_wall = tk.PhotoImage(file=f'assets/{folder}/right_wall.png')
        self.bottom_wall = tk.PhotoImage(file=f'assets/{folder}/bottom_wall.png')

        self.red_slot = tk.PhotoImage(file=f'assets/{folder}/red_slot.png')
        self.empty_slot = tk.PhotoImage(file=f'assets/{folder}/empty_slot.png') 
        self.orange_slot = tk.PhotoImage(file=f'assets/{folder}/orange_slot.png')

        self.empty_space = tk.PhotoImage(file=f'assets/{folder}/empty_space.png')
        self.empty_space_edge = tk.PhotoImage(file=f'assets/{folder}/empty_space_edge.png')

        self.red_indicator_bottom = tk.PhotoImage(file=f'assets/{folder}/red_indicator_bottom.png')
        self.orange_indicator_bottom = tk.PhotoImage(file=f'assets/{folder}/orange_indicator_bottom.png')


    def load_image_sequences(self, theme: str):
        '''Creates instances of image files in a list.'''
        if theme == 'dark':
            folder = 'dark_theme'

        elif theme == 'light':
            folder = 'light_theme'

        self.orange_indicator = [tk.PhotoImage(file=f'assets/{folder}/animated/orange_indicator{frame+1}.png') for frame in range(10)]
        self.red_indicator = [tk.PhotoImage(file=f'assets/{folder}/animated/red_indicator{frame+1}.png') for frame in range(10)]

        self.orange_disc_flip = [tk.PhotoImage(file=f'assets/{folder}/animated/orange_disc_flip{frame+1}.png') for frame in range(14)]
        self.red_disc_flip = [tk.PhotoImage(file=f'assets/{folder}/animated/red_disc_flip{frame+1}.png') for frame in range(14)]

        self.red_smoke_reveal = [tk.PhotoImage(file=f'assets/animated/red_smoke_reveal{frame+1}.png') for frame in range(8)]
        self.orange_smoke_reveal = [tk.PhotoImage(file=f'assets/animated/orange_smoke_reveal{frame+1}.png') for frame in range(8)]

        self.red_crown_shine = [tk.PhotoImage(file=f'assets/animated/red_crown_shine{frame+1}.png') for frame in range(16)]
        self.orange_crown_shine = [tk.PhotoImage(file=f'assets/animated/orange_crown_shine{frame+1}.png') for frame in range(16)]


    def create_frames(self):
        '''Creates frames and set image files.'''
        self.main_frame = tk.Frame(self)
        self.top_wall_frame = Wall(self.main_frame, self.top_wall)
        self.center_frame = tk.Frame(self.main_frame)
        self.left_wall_frame = Wall(self.center_frame, self.left_wall).pack(side=tk.LEFT)
        self.grid = Grid(self.center_frame, self.empty_slot, self.slots).pack(side=tk.LEFT)
        self.right_wall_frame = Wall(self.center_frame, self.right_wall).pack(side=tk.LEFT)
        self.bottom_wall_frame = Wall(self.main_frame, self.bottom_wall)

        self.create_piece_view()


    def create_layout(self):
        '''Places the frames in the screen.'''
        self.piece_view.pack(side=tk.TOP, fill='none', expand=False)
        self.top_wall_frame.pack(side=tk.TOP)
        self.center_frame.pack(side=tk.TOP)
        self.bottom_wall_frame.pack(side=tk.TOP)
        self.main_frame.pack(fill='none', expand=True)


    def bind_click_event(self, action):
        '''
        Binds a mouse click event to each slot.\n
        The event calls the specified function and passes in the coordinates of the clicked slot.
        '''
        for row in range(6):
            for col in range(7):
                self.slots[row][col].bind('<Button-1>', lambda event, x=row, y=col: action(x,y))


    def bind_hover_event(self, show, hide):
        '''Binds a hover event fo every slot.'''
        for row in range(6):
            for col in range(7):
                self.slots[row][col].bind('<Enter>', lambda event, col=col: show(col))
                self.slots[row][col].bind('<Leave>', lambda event, col=col: hide(col))


    def bind_spacebar_event(self, reset):
        '''Binds a spacebar key press event.'''
        self.bind('<Key>', lambda event: reset(True if event.keysym == 'space' else False))



    def fill_slot(self, pos: tuple[int, int], turn: int):
        '''Places a piece of the specified color at the specified position.'''
        x, y = pos[0], pos[1]

        if turn == 1:
            image = self.red_slot
        elif turn == 2:
            image = self.orange_slot

        self.slots[x][y]['image'] = image


    def reset(self):
        for row in range(6):
            for col in range(7):
                self.slots[row][col]['image'] = self.empty_slot


    def create_piece_view(self):
        '''Creates the frame for the piece indicator.'''
        self.columns = [None for col in range(7)]
        self.piece_view = PieceView(self.main_frame, self.empty_space, self.columns)

        ImgLabel(self.piece_view, image=self.empty_space_edge).grid(row=0, column=0)
        ImgLabel(self.piece_view, image=self.empty_space_edge).grid(row=0, column=8)


    def start_animation(self, image_label, image_sequence:list, loop:bool = False, fps:int = 15, current_frame:int = 0) -> bool:
        '''Changes the image on the image label at set interval.'''
        image_label['image'] = image_sequence[current_frame]

        total_frames = len(image_sequence)

        if current_frame < total_frames-1:
            current_frame += 1
        elif loop:
            current_frame = 0
        else:
            return True

        stop_id = self.after(1000//fps, self.start_animation,
                                  image_label,
                                  image_sequence,
                                  loop,
                                  fps,
                                  current_frame)

        if loop:
            self.store_id(stop_id)


    def stop_animation(self):
        for i in self.stop_ids:
            self.after_cancel(i)


    def reset_board(self, game_array: list[list[int]]):
        '''Resets the slots one by one in a random order and plays an animation for each of them.'''
        occupied_slots = self.get_occupied_slots(game_array)
        self.reset_animation(occupied_slots)


    def get_occupied_slots(self, game_array: list[list[int]]) -> list[tuple[int, int, int]]:
        '''Returns a list of tuples containing the position of every occupied slot and the player occupying it.'''
        occupied_slots = []

        for row in range(6):
            for col in range(7):
                if game_array[row][col].player != 0:
                    occupied_slots.append((row, col, game_array[row][col].player))

        return occupied_slots


    def reset_animation(self, occupied_slots:list[tuple[int, int]]):
        '''Plays the reset animation for every occupied slot.'''
        for pos in occupied_slots:
            x, y = pos[0], pos[1]
            player = pos[2]

            if player == 1:
                image_sequence = self.red_disc_flip
            elif player == 2:
                image_sequence = self.orange_disc_flip

            self.start_animation(self.slots[x][y], image_sequence)


    def show_winner(self, winner_segment:list[tuple[int, int]], turn: int):
            if turn == 1:
                image_sequence1 = self.red_smoke_reveal
                image_sequence2 = self.red_crown_shine

            elif turn == 2:
                image_sequence1 = self.orange_smoke_reveal
                image_sequence2 = self.orange_crown_shine

            for pos in winner_segment:
                x, y = pos[0], pos[1]
                self.start_animation(self.slots[x][y], image_sequence1, False, 12)
                self.after(500, self.start_animation, self.slots[x][y], image_sequence2, True, 6)


    def store_id(self, identifier: str):
        '''Stores the after functions identifiers.'''
        self.stop_ids.append(identifier)




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
    def __init__(self, parent, image, slots: list[list[int]]):
        super().__init__(parent)
        for row in range(6):
            for col in range(7):
                slots[row][col] = ImgLabel(self, image)
                slots[row][col].grid(row=row, column=col)


class Wall(tk.Frame):
    '''Creates a frame and places an image inside of it.'''
    def __init__(self, parent, image):
        super().__init__(parent)
        ImgLabel(self, image).pack()


class PieceView(tk.Frame):
    '''Creates a frame and places a grid of image labels inside of it.'''
    def __init__(self, parent, image, columns: list[list[int]]):
        super().__init__(parent)
        for col in range(7):
            columns[col] = ImgLabel(self, image)
            columns[col].grid(row=0, column=col+1)



def main():
    display = Display('light')
    






    display.mainloop()



if __name__ == '__main__':
    main()