from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line
from kivy.graphics.context_instructions import Color

class Tile(Widget):
    def __init__(self,**kwargs):
        super(Tile, self).__init__(**kwargs)
        
        self.color = (1, 1, 1, 1)
        self.borders = [True, True]
        self.borderColor = (0, 0, 0, 1)
        self.borderWidth = 1
        
        self.bind(pos = self.render)
        self.bind(size = self.render)

    def render(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            Rectangle(pos=self.pos, size=self.size)

        self.renderBorders()

    def renderBorders(self):
        # top border
        if self.borders[0] == True:
            with self.canvas:
                Color(*self.borderColor)
                Line(
                    points=[
                        self.pos[0], self.pos[1] + self.height,
                        self.pos[0] + self.width, + self.height + self.pos[1]
                    ],
                    width=self.borderWidth,
                )

        # right Border
        if self.borders[1] == True:
            with self.canvas:
                Color(*self.borderColor)
                Line(
                    points=[
                        self.pos[0] + self.width, self.pos[1],
                        self.pos[0] + self.width, self.pos[1] + self.height
                    ],
                    width=self.borderWidth,
                )

    def getPosition(self):
        return self.pos

    def setSize(self, width, height, instance = None):
        self.size = (width, height)

    def getSize(self):
        return self.size

    def setColor(self, color):
        self.color = color
        self.render()

    def setBorderColor(self, color):
        self.borderColor = color
        self.render()

    def setBorders(self, index, value):
        self.borders[index] = value
        self.render()

    def setBorderWidth(self, borderWidth):
        self.borderWidth = borderWidth
        self.render()

    def getBorders(self):
        return self.borders
    
    def getIndex(self):
        num = self.parent.children.index(self)
        num = self.parent.rows*self.parent.cols - num - 1
        
        i = num//self.parent.cols
        j = num % self.parent.cols
        return [i,j]
    
    def on_touch_down(self, touch):
        if self.parent.chooseEnd == True:
            if self.collide_point(*touch.pos):
                self.parent.chooseEnd = False
                self.parent.changeGoal(self.getIndex())
                
        elif self.parent.chooseStart == True:
            if self.collide_point(*touch.pos):
                self.parent.chooseStart = False
                self.parent.changeStart(self.getIndex())
            
                
