import tkinter as tk
from animation import load_frames


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
        self.red_smoke = load_frames(f'assets/sprites/default/smoke/red_smoke')
        self.orange_smoke = load_frames(f'assets/sprites/default/smoke/orange_smoke')

        # crown glimmer animation
        self.red_crown = load_frames(f'assets/sprites/default/crown/red_crown')
        self.orange_crown = load_frames(f'assets/sprites/default/crown/orange_crown')

        # indicator animation
        self.orange_indicator = load_frames(f'assets/sprites/{self.theme}/animated/orange_indicator')
        self.red_indicator = load_frames(f'assets/sprites/{self.theme}/animated/red_indicator')

        # starting fall animation (top)
        self.o_fall_top_start = load_frames(f'assets/sprites/{self.theme}/animated/o_fall_top_s')
        self.r_fall_top_start = load_frames(f'assets/sprites/{self.theme}/animated/r_fall_top_s')

        # starting fall animation
        self.oo_fall_start = load_frames(f'assets/sprites/{self.theme}/animated/oo_fall_s')
        self.or_fall_start = load_frames(f'assets/sprites/{self.theme}/animated/or_fall_s')

        self.ro_fall_start = load_frames(f'assets/sprites/{self.theme}/animated/ro_fall_s')
        self.rr_fall_start = load_frames(f'assets/sprites/{self.theme}/animated/rr_fall_s')

        # fall animation (top)
        self.o_fall_top = load_frames(f'assets/sprites/{self.theme}/animated/o_fall_top')
        self.r_fall_top = load_frames(f'assets/sprites/{self.theme}/animated/r_fall_top')

        # fall animation (bottom)
        self.o_fall_bot = load_frames(f'assets/sprites/{self.theme}/animated/o_fall_bot')
        self.r_fall_bot = load_frames(f'assets/sprites/{self.theme}/animated/r_fall_bot')

        # fall animation
        self.oo_fall = load_frames(f'assets/sprites/{self.theme}/animated/oo_fall')
        self.or_fall = load_frames(f'assets/sprites/{self.theme}/animated/or_fall')

        self.ro_fall = load_frames(f'assets/sprites/{self.theme}/animated/ro_fall')
        self.rr_fall = load_frames(f'assets/sprites/{self.theme}/animated/rr_fall')

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


class Image(tk.PhotoImage):
    def __init__(self, file_name: str, theme: str):
        super().__init__(file=f'assets/sprites/{theme}/{file_name}.png')


if __name__ == '__main__':
    test = tk.Tk()


    Graphics('dark')



    ...