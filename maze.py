from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
from controllers.maze_controller import MazeController

class Maze(GridLayout):
    def __init__(self, rows, cols, buttons, **kwargs):
        super(Maze, self).__init__(**kwargs)
        
        self.buttons = buttons
        self.rows = rows
        self.cols = cols
        self.tiles = [[None for j in range(self.cols)] for i in range(self.rows)]
        
        self.player = None
        self.playerColor = (116/255, 133/255, 101/255,1)     

        self.goalColor = (0,1,0,1)
        
        self.defaultColor = (1,1,1,1)
        self.defaultBorderColor = (0,0,0,1)
        
        self.tileColor = (26/255, 58/255, 69/255,1)
        self.borderColor = (0.8,0.8,0.8,1)
        self.correctPathColor = (205/255, 84/255, 29/255,0.5)
        # self.visitedColor = (56/255, 104/255, 88/255,1)
        # self.visitedColor = (0/255, 203/255, 247/255,1)
        self.visitedColor = (0, 0, 0,1)
        
        self.currentPos = (0, 0)
        self.startPos = [0, 0]
        self.goalPos = [self.rows - 1, self.cols - 1]
        
        self.chooseStart = self.chooseEnd = False
        
        MazeController.update_rows_cols(self,self.rows,self.cols)
        
    def _render(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].setSize(self.width / self.rows, self.height / self.cols)
            
    def _renderPlayer(self, *args):
        if self.player is not None:
            self.canvas.remove(self.player)
        
        i, j = self.currentPos

        tilePos = self.tiles[i][j].getPosition()
        tileSize = self.tiles[i][j].getSize()
        
        playerPos = (tilePos[0] + tileSize[0]/4, tilePos[1] + tileSize[1]/4)
        playerSize = (tileSize[0]/2, tileSize[1]/2)
        
        with self.canvas:
            Color(*self.playerColor)
            self.player = Rectangle(pos = playerPos, size = playerSize)
            
    def setPosition(self, pos):
        self.pos = pos
        # self._render()
    
    def resize(self, size, *args):
        self.size_hint = (None, None)
        self.size = size
     
    def _resetColors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].setColor(self.tileColor)
   
        i,j = self.goalPos
        self.tiles[i][j].setColor(self.goalColor)
            
    def initLabels(self, stepsLabel):
        self.stepsLabel = stepsLabel
        self.stepsLabel.text = f'Steps: {0}'