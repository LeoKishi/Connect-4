import tkinter as tk
import glob

class Animation(tk.Label):
    def __init__(self, display:tk.Tk, parent:tk.Frame = None):
        super().__init__(parent,
                         relief=tk.FLAT,
                         borderwidth=0,
                         highlightthickness=0)

        self.display = display
        self.sequence = dict()

        # list to store tkinter 'after' function identificators
        self.stop_ids = list()


    def play(self, name:str, loop:bool = False, fps:int = 15):
        '''Stops the previous sequence then starts the current one.'''
        self.stop()
        self._start_animation(name, loop, fps)


    def _start_animation(self, name:str, loop:bool, fps:int, _frame:int = 0):
        '''Cycles through a list of images and displays them at set intervals.'''

        # set current frame
        self['image'] = self.sequence[name][_frame]

        # frame counter
        if _frame < len(self.sequence[name])-1:
            _frame += 1
        elif loop:
            _frame = 0
        else:
            return True

        # clear previous identifier
        if self.stop_ids:
            self.stop_ids.pop()

        # recursion
        stop_id = self.display.after(1000//fps, self._start_animation, name, loop, fps, _frame)
        self.stop_ids.append(stop_id)


    def stop(self):
        '''Stops the animation.'''
        if self.stop_ids:
            self.display.after_cancel(self.stop_ids.pop())


    def timer(self, ms:int = 0):
        '''After set amount of time the animation stops.'''
        self.display.after(ms, self.stop)


    def schedule(self, name:str, ms:int = 0, sec:float = 0, loop:bool = False, fps:int = 15):
        '''Plays the next animation after set amount of time.'''
        if sec:
            time = int(sec*1000)
        else:
            time = ms

        self.display.after(time, self.play, name, loop, fps)


    def load(self, name: str, directory: str):
        '''Saves an animation sequence.'''
        self.sequence[name] = self._load_frames(directory)


    def _load_frames(self, directory: str) -> list[tk.PhotoImage]:
        '''Create a list with every frame of the animation.'''
        frames = list()

        for file in self._get_files(directory):
            frames.append(tk.PhotoImage(file=f'{directory}/{file}.png'))
        
        return frames


    def _get_files(self, directory: str) -> list[str]:
        '''Returns a sorted list with the name of every file in the directory.'''
        file_names = list()

        # list all png files in directory
        for name in glob.glob(f'{directory}/*.png'):
            file_names.append(name[len(directory)+1:-4])
        
        # sort files by frame number
        name_len = len(file_names[0][:-1])
        file_names.sort(key=lambda frame: int(frame[name_len:]))

        return file_names




if __name__ == '__main__':
    main_window = tk.Tk()
    frame1 = tk.Frame(main_window, height=300, width=300, bg='white')


    test = Animation(display=main_window, parent=frame1)
    test.pack()
    
    test.load('red_crown', 'assets/sprites/default/crown/red_crown')
    test.load('name', 'assets/sprites/default/smoke/orange_smoke')

    test.play('red_crown', loop=True, fps=12)
    test.schedule('name', ms=3500, loop=False, fps=12)


    frame1.pack()
    frame1.pack_propagate(0)
    main_window.mainloop()
    ...