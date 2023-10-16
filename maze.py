from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
import random
import time
import threading
from kivy.core.window import Window


from tile import Tile

class Maze(GridLayout):
    def __init__(self, rows, cols, size, **kwargs):
        super(Maze, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.minimum_size = size
        # self.pos_hint = {'center_x': .5, 'center_y': .5}        
        self.pos = (0, Window.height - self.size[1])
        self.rows = rows
        self.cols = cols
        self.size = size
        
        self.tiles = [[None for i in range(self.cols)] for j in range(self.rows)]
        self.visited = []
        
        self.player = None
        self.playerColor = (0,0,1,1)     
        
        self.currentPos = (2,2)
        
        self.defaultColor = (1,1,1,1)
        self.defaultBorderColor = (0,0,0,1)
        
        self.tileColor = (0.5,0.5,0.5,1)
        self.borderColor = (1,1,0,1)
        
        for i in range(self.rows):
            for j in range(self.cols):
                tile = Tile(self.size[0] / self.rows, self.size[1] / self.cols)
                print(self.pos)
                tile.setPosition(i * self.size[0] / self.rows + self.pos[0], j * self.size[1] / self.cols + self.pos[1])
                self.tiles[i][j] = tile
                self.add_widget(tile)

        self.__clearMaze()        
        self.renderPlayer()
        
    
    def renderPlayer(self):
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
        self.renderPlayer()
    
    def resize(self, size):
        self.size = size
        # self.render()
                
    def __clearMaze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].color = self.defaultColor
                self.tiles[i][j].borderColor = self.defaultBorderColor
                self.tiles[i][j].setBorders(0, True)
                self.tiles[i][j].setBorders(1, True)
            
    def generateMaze(self, instance = None):
        print(self.pos)

        self.__clearMaze()
        self.visited = [[False for i in range(self.cols)] for j in range(self.rows)]
        
        i = random.randint(0, self.rows - 1)
        j = random.randint(0, self.cols - 1)
        
        self.__generateMaze(i, j)
    
    def __generateMaze(self, i, j):
        
        while True:
            
            # Mark the current cell as visited
            self.visited[i][j] = True
            self.tiles[i][j].setColor(self.tileColor)
            self.tiles[i][j].setBorderColor(self.borderColor)
            
            # Update player position on screen
            self.currentPos = (i,j)
            self.renderPlayer()
            
            # Get the unvisited neighbours of the current cell
            neighbours_unvisited = self.neighbours_unvisited(i, j)
            
            if len(neighbours_unvisited) == 0:
                return
            
            neighbour = random.choice(neighbours_unvisited)
            
            # Remove the wall between the current cell and the chosen cell
            nbrI = neighbour[0]
            nbrJ = neighbour[1]

            self.__remove_wall(i, j, nbrI, nbrJ)
            
            self.__generateMaze(nbrI, nbrJ)

    def __remove_wall(self, i, j, nbrI, nbrJ):
                
        nbr2I = nbrI
        nbr2J = nbrJ

        if nbrI == i:
            wall = 1
            nbr2I = i
            if nbrJ == j + 1:
                nbr2J = j
        else:
            wall = 0
            nbr2J = j
            if nbrI == i - 1:
                nbr2I = i
        
        self.tiles[i][j].setBorders(wall, False)
        
        self.tiles[nbr2I][nbr2J].setBorders(wall, False)
        
        # time.sleep(2)        
    
    def neighbours_unvisited(self, i, j):
        
        neighbors = []

        # Check the bottom neighbor
        if i + 1 < self.rows and not self.visited[i + 1][j]:
            neighbors.append([i + 1, j])

        # Check the top neighbor
        if i - 1 >= 0 and not self.visited[i - 1][j]:
            neighbors.append([i - 1, j])

        # Check the right neighbor
        if j + 1 < self.cols and not self.visited[i][j + 1]:
            neighbors.append([i, j + 1])

        # Check the left neighbor
        if j - 1 >= 0 and not self.visited[i][j - 1]:
            neighbors.append([i, j - 1])

        return neighbors
    



