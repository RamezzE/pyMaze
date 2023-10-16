from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
# from kivy.core.window import Window

from tile import Tile

class Maze(BoxLayout):
    def __init__(self, rows, cols, size, **kwargs):
        super(Maze, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.rows = rows
        self.cols = cols
        self.size = size
        self.pos = (0, 0)
        
        self.render()
        
    def render(self):
        for i in range(self.rows):
            for j in range(self.cols):
                tile = Tile(self.size[0] / self.rows, self.size[1] / self.cols)
                tile.setPosition(i * self.size[0] / self.rows, j * self.size[1] / self.cols)
                self.add_widget(tile)
                
    



