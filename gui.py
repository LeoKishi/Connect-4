import tkinter as tk
from tkinter import ttk


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

        self.load_images(theme)
        self.load_image_sequences(theme)
        self.create_frames()
        self.create_layout()


    def load_images(self, theme: str):
        '''Creates instances of the image files.'''
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
        self.orange_indicator = [None for i in range(10)]
        self.red_indicator = [None for i in range(10)]

        if theme == 'dark':
            folder = 'dark_theme'

        elif theme == 'light':
            folder = 'light_theme'

        for frame in range(10):
            self.orange_indicator[frame] = tk.PhotoImage(file=f'assets/{folder}/animated/orange_indicator{frame+1}.png')
            self.red_indicator[frame] = tk.PhotoImage(file=f'assets/{folder}/animated/red_indicator{frame+1}.png')


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

        empty_label_1 = tk.Label(self.piece_view, image=self.empty_space_edge, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        empty_label_2 = tk.Label(self.piece_view, image=self.empty_space_edge, relief=tk.FLAT, borderwidth=0, highlightthickness=0)

        empty_label_1.grid(row=0, column=0)
        empty_label_2.grid(row=0, column=8)


    def start_animation(self, image_label, image_sequence:list, total_frames:int, current_frame:int = 0, fps:int = 15):
        '''Changes the image on the image label at set interval.'''
        image_label['image'] = image_sequence[current_frame]

        if current_frame < total_frames-1:
            current_frame += 1
        else:
            current_frame = 0

        self.stop_id = self.after(1000//fps, self.start_animation,
                                  image_label,
                                  image_sequence,
                                  total_frames,
                                  current_frame)


    def stop_animation(self):
        self.after_cancel(self.stop_id)






class Grid(tk.Frame):
    '''Creates a frame and places a grid of image labels inside of it.'''
    def __init__(self, parent, image, slots: list[list[int]]):
        super().__init__(parent)
        for row in range(6):
            for col in range(7):
                slots[row][col] = tk.Label(self,
                                           image=image,
                                           relief=tk.FLAT,
                                           borderwidth=0,
                                           highlightthickness=0)
                slots[row][col].grid(row=row, column=col)


class Wall(tk.Frame):
    '''Creates a frame and places an image inside of it.'''
    def __init__(self, parent, image):
        super().__init__(parent)
        tk.Label(self,
                 image=image,
                 relief=tk.FLAT,
                 borderwidth=0,
                 highlightthickness=0).pack()


class PieceView(tk.Frame):
    '''Creates a frame and places a grid of image labels inside of it.'''
    def __init__(self, parent, image, columns: list[list[int]]):
        super().__init__(parent)
        for col in range(7):
            columns[col] = tk.Label(self,
                                        image=image,
                                        relief=tk.FLAT,
                                        borderwidth=0,
                                        highlightthickness=0)
            columns[col].grid(row=0, column=col+1)



def main():
    display = Display('light')
    






    display.mainloop()



if __name__ == '__main__':
    main()