from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line
from kivy.graphics.context_instructions import Color


class Tile(Widget):
    def __init__(self, height, width, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.size = (width, height)
        self.color = (1, 1, 1, 1)

        self.borders = [True, True]
        self.borderColor = (0, 0, 0, 1)
        self.rightBorder = self.bottomBorder = None
        self.borderWidth = 0.5

        self.render()

    def render(self):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            Rectangle(pos=self.pos, size=self.size)

            self.renderBorders()

    def renderBorders(self):
        # right Border
        if self.rightBorder is not None:
            self.canvas.remove(self.rightBorder)
            
        if self.borders[0] == True:
            with self.canvas:
                Color(*self.borderColor)
                Line(
                    points=[
                        self.pos[0] + self.size[0], self.pos[1],
                        self.pos[0] + self.size[0], self.pos[1] + self.size[1]
                    ],
                    width=self.borderWidth,
                )

        # bottom border
        if self.bottomBorder is not None:
            self.canvas.remove(self.bottomBorder)
            
        if self.borders[1] == True:
            with self.canvas:
                Color(*self.borderColor)
                Line(
                    points=[
                        self.pos[0], self.pos[1],
                        self.pos[0] + self.size[0], self.pos[1]
                    ],
                    width=self.borderWidth,
                )

    def setPosition(self, x, y):
        self.pos = (x, y)
        self.render()

    def getPosition(self):
        return self.pos

    def setSize(self, width, height):
        self.size = (width, height)
        self.render()

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
