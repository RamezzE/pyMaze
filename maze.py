from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
import random
import time
import threading


from tile import Tile

class Maze(BoxLayout):
    def __init__(self, rows, cols, size, **kwargs):
        super(Maze, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.rows = rows
        self.cols = cols
        self.size = size
        self.pos = (0, 0)
        
        self.tiles = [[None for i in range(self.cols)] for j in range(self.rows)]
        self.visited = [[False for i in range(self.cols)] for j in range(self.rows)]
        
        self.player = None
        self.playerColor = (0,0,1,1)     
        
        self.currentPos = (2,2)
        
        self.defaultColor = (1,1,1,1)
        self.defaultBorderColor = (0,0,0,1)
        
        self.tileColor = (0.2,0.6,0.7,1)
        self.borderColor = (0,1,0,1)
        
        for i in range(self.rows):
            for j in range(self.cols):
                tile = Tile(self.size[0] / self.rows, self.size[1] / self.cols)
                tile.setPosition(i * self.size[0] / self.rows + self.pos[0], j * self.size[1] / self.cols + self.pos[1])
                self.tiles[i][j] = tile
                self.add_widget(tile)
        
        self.render()
        
    def render(self):
        # self.canvas.clear()
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].setPosition(i * self.size[0] / self.rows + self.pos[0], j * self.size[1] / self.cols + self.pos[1])
                # self.canvas.remove(self.tiles[i][j].)
                # self.tiles[i][j].render()
                
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
            Rectangle(pos = playerPos, size = playerSize)
            
    def setPosition(self, pos):
        self.pos = pos
        self.render()
    
    def resize(self, size):
        self.size = size
        self.render()
                
    def __clearMaze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].color = self.defaultColor
                self.tiles[i][j].borderColor = self.defaultBorderColor
        
        self.render()
    
    def generateMaze(self):
        self.__clearMaze()
        
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
            self.render()
            
            # Get the unvisited neighbours of the current cell
            neighbours_unvisited = self.neighbours_unvisited(i, j)
            
            if len(neighbours_unvisited) == 0:
                return
            
            neighbour = random.choice(neighbours_unvisited)
            
            print(neighbours_unvisited)
            print(neighbour)
            
            # Remove the wall between the current cell and the chosen cell
            nbrI = neighbour[0]
            nbrJ = neighbour[1]

            self.__remove_wall(i, j, nbrI, nbrJ)
            
            self.__generateMaze(nbrI, nbrJ)

    def __remove_wall(self, i, j, nbrI, nbrJ):
        
        # print("Removing wall between: ", i, j, " and ", nbrI, nbrJ)
        
        nbr2J = nbrJ
        nbr2I = nbrI

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
        # self.tiles[i][j].renderBorders()
        
        self.tiles[nbr2I][nbr2J].setBorders(wall, False)
        # self.tiles[nbr2I][nbr2J].renderBorders()
        
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
    



