import tkinter as tk
import random
import wincondition

class Button:
    def __init__(self):
        self.height = 6
        self.width = 7
        self.buttons = [[col for col in range(self.width)] for row in range(self.height)] # tkinter buttons
        self.array = [[col for col in range(self.width)] for row in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                self.array[row][col] = 0
                self.array[row][col] = Square(row, col) # turning array elements into class to hold information
                self.buttons[row][col] = tk.Button(grid,
                                                    font= ('', '20', 'bold'),
                                                    height= 1, width= 3,
                                                    relief= tk.SUNKEN,
                                                    borderwidth= 6,
                                                    bg= '#79abf2',
                                                    command= (lambda x=row, y=col: control.select(x,y)))
                self.buttons[row][col].grid(row=row+1,column=col, padx=(3,3), pady=(3,3))
                self.buttons[row][col].bind('<Enter>', lambda event, column=col: visual.show_next_piece(column))
                self.buttons[row][col].bind('<Leave>', lambda event, column=col: visual.hide_next_piece(column))

class Square:
    def __init__(self, x, y):
        self.pos = [x,y] # position in the array
        self.player = None # which player is occupying this square

    def get_pos(self):
        return self.pos

class Control:
    def __init__(self):
        self.turn = random.randint(1,2) # randomize first turn / 1 for player 1 and 2 for player 2

    def select(self, x, y): # chooses the bottom-most available square in the selected colummn
        for col in range((button.height-1), -1, -1):
            if button.array[col][y].player == None:
                self.move(col, y)
                return

    def move(self, x, y): # place a piece in the selected square
        # player 1 (red)
        if self.turn == 1:
            button.array[x][y].player = 1
            button.buttons[x][y]['bg'] = 'red'
            if (search.search_winner(button.array, self.turn) == True):
                self.pause()
                visual.blink_segment(search.winning_segment)
                return
            self.turn = 2
            visual.show_next_piece(y) # refresh next piece indicator
            return
        # player 2 (orange)
        elif self.turn == 2:
            button.array[x][y].player = 2
            button.buttons[x][y]['bg'] = 'orange'
            if (search.search_winner(button.array, self.turn) == True):
                self.pause()
                visual.blink_segment(search.winning_segment)
                return
            self.turn = 1
            visual.show_next_piece(y) # refresh next piece indicator
            return

    def pause(self):
        for row in range(button.height):
            for col in range(button.width):
                button.buttons[row][col]['command'] = '' # remove button function
                
    def reset(self):
        if len(visual.stop_list) > 0:
            for item in visual.stop_list:
                window.after_cancel(item) # stops after() functions from blinking animation
        for row in range(button.height):
            for col in range(button.width):
                button.array[row][col] = 0 # clear array
                button.array[row][col] = Square(row, col) 
                button.buttons[row][col]['bg'] = '#79abf2' # default tkinter color
                button.buttons[row][col]['command'] = (lambda x=row, y=col: control.select(x,y)) # reassign function to button
        self.turn = random.randint(1,2) # randomize first turn

class Visual:
    def __init__(self):
        # top row of squares displaying next piece
        self.display = [row for row in range(button.width)]
        for col in range(button.width):
            self.display[col] = tk.Button(top_frame,
                            font= ('', '20', 'bold'),
                            text= (col+1),
                            height= 1, width= 3,
                            relief= tk.FLAT,
                            fg= '#5b88c9',
                            bg= '#79abf2',
                            state= 'disabled')
            self.display[col].grid(row=0, column=col,padx=(7,7), pady=(7,4))
        self.stop_list = []

    def show_next_piece(self, col):
        if control.turn == 1:
            self.display[col]['bg'] = 'red'
            self.display[col]['text'] = ''
            self.display[col]['relief'] = tk.RAISED
        else:
            self.display[col]['bg'] = 'orange'
            self.display[col]['text'] = ''
            self.display[col]['relief'] = tk.RAISED
    
    def hide_next_piece(self, col):
        self.display[col]['bg'] = '#79abf2'
        self.display[col]['text'] = (col+1)
        self.display[col]['relief'] = tk.FLAT

    def blink_segment(self, segment):
        self.show_segment(segment)

    def show_segment(self, segment):
        for square in segment:
            x = square[0]
            y = square[1]
            if control.turn == 1:
                button.buttons[x][y]['bg'] = 'red'
            else:
                button.buttons[x][y]['bg'] = 'orange'
        self.stop_list.append(window.after(400, lambda segment=segment: self.hide_segment(segment)))

    def hide_segment(self, segment):
        for square in segment:
            x = square[0]
            y = square[1]
            button.buttons[x][y]['bg'] = 'white'
        self.stop_list.append(window.after(200, lambda segment=segment: self.show_segment(segment)))

# root
window = tk.Tk()
window.resizable(0,0)
window.title('Connect 4')
window.configure(bg= '#588cd6')

# frame creation
header_frame = tk.Frame(window, relief=tk.RIDGE, borderwidth=6)
title_frame = tk.Frame(header_frame)
top_frame = tk.Frame(window, relief=tk.SUNKEN, borderwidth=6, bg= '#79abf2')
main_frame = tk.Frame(window)
bottom_frame = tk.Frame(window)
grid = tk.Frame(main_frame, bg= '#588cd6')

# frame packing
header_frame.pack(fill=('x'))
title_frame.pack()
top_frame.pack(pady=(20,0))
main_frame.pack(padx=(20,20),pady=(20,20))
bottom_frame.pack(pady=(0,20))
grid.pack()

# class instances
button = Button()
control = Control()
search = wincondition.Check(button.height, button.width)
visual = Visual()

# widget creation
title_connect = tk.Label(title_frame, font=('Consolas', '60', 'bold'),
                 text= 'Connect')
title_4 = tk.Label(title_frame, font=('Consolas', '80', 'bold'),
                 text= '4',
                 fg= 'red')

reset_button = tk.Button(bottom_frame,
                        font= ('Consolas', '15', 'bold'),
                        text= 'RESET',
                        relief= tk.RAISED,
                        borderwidth= 3,
                        bg= '#bfd1e0',
                        command= control.reset)

# widget packing
title_connect.pack(side=tk.LEFT, anchor='e')
title_4.pack(side=tk.RIGHT, anchor='w')
reset_button.pack(side=tk.BOTTOM)

window.mainloop()