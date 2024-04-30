import tkinter as tk
from typing import Callable


class Sprite(tk.Label):
    '''
    Custom Tkinter Label class to play animations.\n

    The play( ) method can be used to play a specific sequence or to start the queued animations.\n

    The animation can be stopped at any time with the stop( ) method\n

    Animations can be queued with the chain( ) method.
        If the animation is running, the next sequence plays when 
        the previous one automatically stops or if the next( ) method is called manually.

    '''
    def __init__(self, main_window:tk.Tk, master:tk.Frame = None, image:tk.PhotoImage = None):
        super().__init__(master, image=image, relief=tk.FLAT, borderwidth=0, highlightthickness=0)

        self.root = main_window
        self.stop_id = None
        self.queue = list()
    

    def play(self, sequence:list[tk.PhotoImage] = None, loop:bool = False, fps:int = 15, timer:int = None):
        '''Plays the given sequence or the items on queue.'''
        if sequence:
            self.stop()
            self._start_animation(sequence, loop, fps)
            if timer is not None:
                self.root.after(timer, self.next)
        else:
            self.next()


    def stop(self):
        '''Stops the animation'''
        if self.stop_id:
            self.root.after_cancel(self.stop_id)


    def chain(self, sequence:list[tk.PhotoImage], timer:int = None, loop:bool = False, fps:int = 15):
        '''Adds a animation to the queue.'''
        self.queue.append((sequence, loop, fps, timer))


    def chain_image(self, image:tk.PhotoImage, timer:int = None):
        '''Adds a image to the queue.'''
        self.queue.append((image, timer))


    def chain_func(self, func:Callable, timer:int = None):
        '''Adds a function to the queue.'''
        self.queue.append((func, timer))


    def next(self):
        '''Jumps to the next item in the queue.'''
        self.stop()

        if not self.queue:
            return

        self._handle_queue()


    def clear_queue(self):
        self.queue = list()


    def _handle_queue(self):
        '''Handles the different types of items in the queue.'''
        item = self.queue[0][0]
        info = self.queue.pop(0)

        if isinstance(item, list):
            self._next_sequence(*info)

        elif isinstance(item, tk.PhotoImage):
            self._next_image(*info)

        elif isinstance(item, Callable):
            self._next_func(*info)


    def _next_sequence(self, sequence:list[tk.PhotoImage], loop:bool, fps:int, timer:int):
        '''Plays the next animation in the queue.'''
        self.play(sequence, loop, fps)

        if timer is not None:
            self.root.after(timer, self.next)


    def _next_image(self, image:tk.PhotoImage, timer:int):
        '''Plays the next image in the queue.'''
        self['image'] = image

        if timer is not None:
            self.root.after(timer, self.next)


    def _next_func(self, func:Callable, timer:int):
        '''Plays the next function in the queue.'''
        func()

        if timer is not None:
            self.root.after(timer, self.next)


    def set_image(self, image:tk.PhotoImage):
        '''Stops any ongoing animation and sets a still image.'''
        self.stop()
        self['image'] = image


    def _start_animation(self, sequence:list[tk.PhotoImage], loop:bool, fps:int, _frame:int = 0):
        '''Starts the animation sequence.'''
        self['image'] = sequence[_frame]

        if _frame < len(sequence)-1:
            _frame += 1
        elif loop:
            _frame = 0
        elif self.queue:
            self.next()
            return
        else:
            return

        if self.stop_id:
            self.stop_id = None

        self.stop_id = self.root.after(1000//fps, self._start_animation, sequence, loop, fps, _frame)
