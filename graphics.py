import tkinter as tk
from glob import glob


class Graphics:
    def __init__(self, display, theme):
        self.display = display

        if theme == 'dark':
            self.theme = 'dark_theme'

        elif theme == 'light':
            self.theme = 'light_theme'

        # list to hold the identifiers of the tkinter after functions 
        self.stop_ids = []

        # create image instances
        self.load_images()
        self.load_image_sequences()


    def start_animation(self,
                        image_label,
                        image_sequence:list,
                        loop:bool = False,
                        fps:int = 15,
                        current_frame:int = 0
                        ) -> bool:
        '''
        Cycles through a list of images and shows each of them in the image label at set intervals.\n
        Arguments:
            display
                Tkinter main window
            image_label
                Tkinter Label class instance
            image_sequence
                list of Tkinter Photoimage class instances with the frames of the animation
            loop
                repeats the animation cycle
            fps
                frames per second
        '''
        image_label['image'] = image_sequence[current_frame]

        if current_frame < len(image_sequence)-1:
            current_frame += 1
        elif loop:
            current_frame = 0
        else:
            return True

        stop_id = self.display.after(1000//fps,
                                self.start_animation,
                                image_label,
                                image_sequence,
                                loop,
                                fps,
                                current_frame)


        self.stop_ids.append(stop_id)


    def stop_animation(self):
        '''Stops all running animations.'''
        while len(self.stop_ids) > 0:
            self.display.after_cancel(self.stop_ids.pop())


    def load_images(self):
        '''Creates instances of image files.'''

        # game border structure
        self.top_wall = Image('top_wall', self.theme)
        self.left_wall = Image('left_wall', self.theme)
        self.right_wall = Image('right_wall', self.theme)
        self.bottom_wall = Image('bottom_wall', self.theme)

        # slots
        self.red_slot = Image('red_slot', self.theme)
        self.empty_slot = Image('empty_slot', self.theme)
        self.orange_slot = Image('orange_slot', self.theme)

        # placeholder for indicators
        self.empty_space = Image('empty_space', self.theme)
        self.empty_space_edge = Image('empty_space_edge', self.theme)

        # indicators
        self.red_indicator_bottom = Image('red_indicator_bottom', self.theme)
        self.orange_indicator_bottom = Image('orange_indicator_bottom', self.theme)


    def load_image_sequences(self):
        '''Creates instances of image files in a list.'''

        # smoke reveal animation
        self.red_smoke = self.load_frames(f'assets/sprites/default/smoke/red_smoke')
        self.orange_smoke = self.load_frames(f'assets/sprites/default/smoke/orange_smoke')

        # crown glimmer animation
        self.red_crown = self.load_frames(f'assets/sprites/default/crown/red_crown')
        self.orange_crown = self.load_frames(f'assets/sprites/default/crown/orange_crown')

        # indicator animation
        self.orange_indicator = self.load_frames(f'assets/sprites/{self.theme}/animated/orange_indicator')
        self.red_indicator = self.load_frames(f'assets/sprites/{self.theme}/animated/red_indicator')

        # starting fall animation (top)
        self.o_fall_top_start = self.load_frames(f'assets/sprites/{self.theme}/animated/o_fall_top_s')
        self.r_fall_top_start = self.load_frames(f'assets/sprites/{self.theme}/animated/r_fall_top_s')

        # starting fall animation
        self.oo_fall_start = self.load_frames(f'assets/sprites/{self.theme}/animated/oo_fall_s')
        self.or_fall_start = self.load_frames(f'assets/sprites/{self.theme}/animated/or_fall_s')

        self.ro_fall_start = self.load_frames(f'assets/sprites/{self.theme}/animated/ro_fall_s')
        self.rr_fall_start = self.load_frames(f'assets/sprites/{self.theme}/animated/rr_fall_s')

        # fall animation (top)
        self.o_fall_top = self.load_frames(f'assets/sprites/{self.theme}/animated/o_fall_top')
        self.r_fall_top = self.load_frames(f'assets/sprites/{self.theme}/animated/r_fall_top')

        # fall animation
        self.oo_fall = self.load_frames(f'assets/sprites/{self.theme}/animated/oo_fall')
        self.or_fall = self.load_frames(f'assets/sprites/{self.theme}/animated/or_fall')

        self.ro_fall = self.load_frames(f'assets/sprites/{self.theme}/animated/ro_fall')
        self.rr_fall = self.load_frames(f'assets/sprites/{self.theme}/animated/rr_fall')

        self.fall_start = {'r':self.r_fall_top_start,
                            'o':self.o_fall_top_start,
                            'rr':self.rr_fall_start,
                            'ro':self.ro_fall_start,
                            'oo':self.oo_fall_start,
                            'or':self.or_fall_start}

        self.fall = {'r':self.r_fall_top,
                    'o':self.o_fall_top,
                    'rr':self.rr_fall,
                    'ro':self.ro_fall,
                    'oo':self.oo_fall,
                    'or':self.or_fall}


    def load_frames(self, directory: str) -> list[tk.PhotoImage]:
        '''Create a list with every frame of the animation.'''
        frames = list()

        for file in self._get_files(directory):
            frames.append(tk.PhotoImage(file=f'{directory}/{file}.png'))

        return frames


    def _get_files(self, directory: str) -> list[str]:
        '''Returns a sorted list with the name of every file in the directory.'''
        file_names = list()

        # list all png files in directory
        for name in glob(f'{directory}/*.png'):
            file_names.append(name[len(directory)+1:-4])
        
        # sort files by frame number
        name_len = len(file_names[0][:-1])
        file_names.sort(key=lambda frame: int(frame[name_len:]))

        return file_names


class Image(tk.PhotoImage):
    def __init__(self, file_name: str, theme: str):
        super().__init__(file=f'assets/sprites/{theme}/{file_name}.png')


class Frame(tk.PhotoImage):
    def __init__(self, file_name: str, frame: int, theme: str = None):
        if theme:
            super().__init__(file=f'assets/sprites/{theme}/{file_name}{frame+1}.png')
        else:
            super().__init__(file=f'assets/sprites/default/{file_name}{frame+1}.png')




if __name__ == '__main__':
    test = tk.Tk()


    Graphics('dark')



    ...