import tkinter as tk
from tkinter import ttk


class Display(tk.Tk):
    '''
    Initializes the game window.\n
    Arguments:
        mode
            'dark' for dark mode. Light mode by default
    '''
    def __init__(self, mode: str = 'light'):
        super().__init__()
        self.minsize(900, 800)
        self.title('Connect 4')

        # list that holds the image labels of the slots
        self.slots = [[col for col in range(7)] for row in range(6)]

        self.load_images(mode)
        self.create_frames()
        self.create_layout()


    def load_images(self, mode: str):
        '''Creates instances of the image files.'''
        if mode == 'dark':
            folder = 'dark_mode'
            self.configure(bg= '#201e23')

        elif mode == 'light':
            folder = 'light_mode'
            self.configure(bg= 'white')

        self.top_wall = tk.PhotoImage(file=f'assets/{folder}/top_wall.png')
        self.left_wall = tk.PhotoImage(file=f'assets/{folder}/left_wall.png')
        self.right_wall = tk.PhotoImage(file=f'assets/{folder}/right_wall.png')
        self.bottom_wall = tk.PhotoImage(file=f'assets/{folder}/bottom_wall.png')

        self.red_slot = tk.PhotoImage(file=f'assets/{folder}/red_slot.png')
        self.empty_slot = tk.PhotoImage(file=f'assets/{folder}/empty_slot.png') 
        self.orange_slot = tk.PhotoImage(file=f'assets/{folder}/orange_slot.png')
        
    def create_frames(self):
        '''Creates the frames with the image files.'''
        self.top_wall_frame = Wall(self, self.top_wall)
        self.center_frame = tk.Frame(self)
        self.left_wall_frame = Wall(self.center_frame, self.left_wall).pack(side=tk.LEFT)
        self.grid = Grid(self.center_frame, self.empty_slot, self.slots).pack(side=tk.LEFT)
        self.right_wall_frame = Wall(self.center_frame, self.right_wall).pack(side=tk.LEFT)
        self.bottom_wall_frame = Wall(self, self.bottom_wall)

    def create_layout(self):
        '''Places the frames in the screen.'''
        self.top_wall_frame.pack(side=tk.TOP)
        self.center_frame.pack(side=tk.TOP)
        self.bottom_wall_frame.pack(side=tk.TOP)

    def bind_function(self, func):
        '''
        Binds a mouse click event to each slot.\n
        The event calls the function and passes in the coordinates of the clicked slot.
        '''
        for row in range(6):
            for col in range(7):
                self.slots[row][col].bind('<Button-1>', lambda event, x=row, y=col: func(x,y))


class Grid(tk.Frame):
    '''Creates a frame and places a grid of buttons inside of it.'''
    def __init__(self, parent, image, slots: list[list[int]]):
        super().__init__(parent)
        height = 6
        width = 7

        for row in range(height):
            for col in range(width):
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
        self.label = tk.Label(self,
                              image=image,
                              relief=tk.FLAT,
                              borderwidth=0,
                              highlightthickness=0)
        self.label.pack()







def main():
    display = Display('light')

    display.mainloop()



if __name__ == '__main__':
    main()