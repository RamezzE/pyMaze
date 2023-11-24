from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color

from tile import Tile

class MazeView(GridLayout):
    def __init__(self, mazeModel, tileOnTouch, **kwargs):
        super(MazeView, self).__init__(**kwargs)
        
        self.mazeModel = mazeModel
        self.tileOnTouch = tileOnTouch
        
        self._tiles = [[None for j in range(self.mazeModel.cols)] for i in range(self.mazeModel.rows)]
        
        self._player = None
        self._playerColor = (116/255, 133/255, 101/255,1)     

        self._goalColor = (0,1,0,1)
        
        self._defaultColor = (1,1,1,1)
        self._defaultBorderColor = (0,0,0,1)
        
        self._tileColor = (26/255, 58/255, 69/255,1)
        self._borderColor = (0.8,0.8,0.8,1)
        self._correctPathPathColor = (205/255, 84/255, 29/255,0.5)
        # self._visitedColor = (56/255, 104/255, 88/255,1)
        # self._visitedColor = (0/255, 203/255, 247/255,1)
        self._visitedColor = (0, 0, 0, 1)
        
        from controllers.maze_controller import MazeController
        MazeController.update_rows_cols(self,self.mazeModel.rows,self.mazeModel.cols)
        
    def render(self):
        for i in range(self.mazeModel.rows):
            for j in range(self.mazeModel.cols):
                self._tiles[i][j].setSize(self.width / self.mazeModel.rows, self.height / self.mazeModel.cols)
            
    def renderPlayer(self, *args):
        if self._player is not None:
            self.canvas.remove(self._player)
        
        i, j = self.mazeModel.getCurrentPos()

        tilePos = self._tiles[i][j].getPosition()
        tileSize = self._tiles[i][j].getSize()
        
        playerPos = (tilePos[0] + tileSize[0]/4, tilePos[1] + tileSize[1]/4)
        playerSize = (tileSize[0]/2, tileSize[1]/2)
        
        with self.canvas:
            Color(*self._playerColor)
            self._player = Rectangle(pos = playerPos, size = playerSize)
    
    def resize(self, size, *args):
        self.size_hint = (None, None)
        self.size = size
    
    def _resetColors(self):
        for i in range(self.mazeModel.rows):
            for j in range(self.mazeModel.cols):
                self._tiles[i][j].setColor(self._tileColor)

        i,j = self.mazeModel.getGoalPos()
        
        self._tiles[i][j].setColor(self._goalColor)
            
    def initLabels(self, stepsLabel):
        self._stepsLabel = stepsLabel
        
    def updateStepsLabel(self, steps):
        self._stepsLabel.text = f'Steps: {steps}'
        
    def clearMaze(self):
        for i in range(1, 6):
            self._buttons[i].disabled = True

        for i in range(self.mazeModel.rows):
            for j in range(self.mazeModel.cols):
                self._tiles[i][j].setColor(self._defaultColor)
                self._tiles[i][j].borderColor = self._defaultBorderColor
                self._tiles[i][j].setBorders(0, True)
                self._tiles[i][j].setBorders(1, True)
                
    def markAsVisited(self, i, j):
        self._tiles[i][j].setColor(self._visitedColor)
    
    def markAsCorrectPath(self, i, j):
        self._tiles[i][j].setColor(self._correctPathPathColor)
      
    def colorGoal(self):
        i,j = self.mazeModel.getGoalPos()
        self._tiles[i][j].setColor(self._goalColor)
        
    def colorBorder(self, i, j):
        self._tiles[i][j].setBorderColor(self._borderColor)
        
    def colorTile(self, i, j):
        self._tiles[i][j].setColor(self._tileColor)

    def enableButtons(self, arr):
        for i in arr:
            self._buttons[i].disabled = False
            
    def disableButtons(self, arr):
        for i in arr:
            self._buttons[i].disabled = True
          
    def setBorder(self, i, j, border, bool):
        self._tiles[i][j].setBorders(border, bool)
            
    def getBorder(self, i, j, border):
        return self._tiles[i][j].getBorders()[border]
    
    def resetMaze(self):
        self.clear_widgets()
        self._tiles = [[None for j in range(self.mazeModel.cols)] for i in range(self.mazeModel.rows)]

        self.rows = self.mazeModel.rows
        self.cols = self.mazeModel.cols
        
        for i in range(self.mazeModel.rows):
            for j in range(self.mazeModel.cols):
                self._tiles[i][j] = Tile(self.tileOnTouch)
                self.add_widget(self._tiles[i][j])
        try:
            for i in range(1, 6):
                self._buttons[i].disabled = True
        except:
            pass

        self.render()
        