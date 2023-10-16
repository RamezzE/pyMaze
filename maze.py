from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color
import random
from kivy.clock import Clock
from functools import partial
from collections import deque


from tile import Tile

class Maze(GridLayout):
    def __init__(self, rows, cols, size, **kwargs):
        super(Maze, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.minimum_size = size
        self.rows = rows
        self.cols = cols
        self.size = size
        
        self.tiles = [[None for i in range(self.cols)] for j in range(self.rows)]
        
        self.player = None
        self.playerColor = (116/255, 133/255, 101/255,1)     
        
        self.currentPos = (2,2)
        
        self.defaultColor = (1,1,1,1)
        self.defaultBorderColor = (0,0,0,1)
        
        self.tileColor = (26/255, 58/255, 69/255,1)
        self.borderColor = (0.8,0.8,0.8,1)
        self.correctPathColor = (205/255, 84/255, 29/255,1)
        self.visitedColor = (56/255, 104/255, 88/255,1)
                
        for i in range(self.rows):
            for j in range(self.cols):
                tile = Tile(self.size[0] / self.rows, self.size[1] / self.cols)
                tile.setPosition(i * self.size[0] / self.rows + self.pos[0], j * self.size[1] / self.cols + self.pos[1])
                self.tiles[i][j] = tile
                self.add_widget(tile)

        self.__clearMaze()        
        self.__renderPlayer()
    
    def __renderPlayer(self, instance = None):
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
        self.__renderPlayer()
    
    def resize(self, size):
        self.size = size
        # self.render()
        
    def __resetColors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].setColor(self.tileColor)
                          
    def __clearMaze(self):        
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].color = self.defaultColor
                self.tiles[i][j].borderColor = self.defaultBorderColor
                self.tiles[i][j].setBorders(0, True)
                self.tiles[i][j].setBorders(1, True)
            
    def generateMaze(self, instance = None):
        print("Generating Maze")
        self.__clearMaze()
        
        # Randomize starting point of maze generation
        
        i = random.randint(0, self.rows - 1)
        j = random.randint(0, self.cols - 1)
        visited = [[False for i in range(self.cols)] for j in range(self.rows)]
        stack = [[i, j]]
        
        self.__generateMazeStep(stack, visited)
        
    def __generateMazeStep(self, stack, visited, instance = None):
        
        if len(stack) == 0:
            return
        
        i, j = stack[-1]
        
        # Mark the current cell as visited
        visited[i][j] = True

        self.tiles[i][j].setColor(self.tileColor)
        self.tiles[i][j].setBorderColor(self.borderColor)
        
        # Update player position on screen
        self.currentPos = (i,j)
        self.__renderPlayer()
        
        # Get the unvisited neighbours of the current cell
        neighbours_unvisited = self.__neighbours_unvisited(i, j, visited)
        
        if len(neighbours_unvisited) == 0:
            stack.pop()
            Clock.schedule_once(partial(self.__generateMazeStep, stack, visited), 0.1)
            return
        
        neighbour = random.choice(neighbours_unvisited)
        
        # Remove the wall between the current cell and the chosen cell
        nbrI = neighbour[0]
        nbrJ = neighbour[1]

        self.__remove_wall(stack[-1], neighbour)
        
        stack.append([nbrI, nbrJ])
        Clock.schedule_once(partial(self.__generateMazeStep, stack, visited), 0.1)
        
    def __remove_wall(self, currentCell, neighbour):
        
        # Same row 
        if currentCell[0] == neighbour[0]:
            wall = 1 # Right or Left Wall to be removed
            i = currentCell[0] = neighbour[0]
            if currentCell[1] > neighbour[1]:
                # Left Wall which is -> Right Wall of Neighbour to be removed
                j = neighbour[1]
            else:
                # Right Wall of currentCell to be removed
                j = currentCell[1]
                
        # Same Column
        else:
            wall = 0 # Top or Bottom Wall to be removed
            j = currentCell[1] = neighbour[1]
            if currentCell[0] < neighbour[0]:
                # Bottom Wall which is -> Top Wall of Neighbour to be removed
                i = neighbour[0]
            else:
                # Top Wall of CurrentCell to be removed
                i = currentCell[0]
                
        self.tiles[i][j].setBorders(wall, False)
                  
    def __neighbours_unvisited(self, i, j, visited):
        
        neighbors = []

        # Check the bottom neighbor
        if i + 1 < self.rows and not visited[i + 1][j]:
            neighbors.append([i + 1, j])

        # Check the top neighbor
        if i - 1 >= 0 and not visited[i - 1][j]:
            neighbors.append([i - 1, j])

        # Check the right neighbor
        if j + 1 < self.cols and not visited[i][j + 1]:
            neighbors.append([i, j + 1])

        # Check the left neighbor
        if j - 1 >= 0 and not visited[i][j - 1]:
            neighbors.append([i, j - 1])

        return neighbors
    
    def __neighbours_unvisited_BFS(self, i, j, visited):
        neighbors = []

        # Check the left neighbor
        if j - 1 >= 0 and not visited[i][j - 1]:
            if not self.tiles[i][j-1].borders[1]:
                neighbors.append([i, j - 1])
            
        # Check the top neighbor
        if i - 1 >= 0 and not visited[i - 1][j]:
            if not self.tiles[i][j].borders[0]:
                neighbors.append([i - 1, j])
            
        # Check the right neighbor
        if j + 1 < self.cols and not visited[i][j + 1]:
            if not self.tiles[i][j].borders[1]:
                neighbors.append([i, j + 1])
            
        # Check the bottom neighbor
        if i + 1 < self.rows and not visited[i + 1][j]:
            if not self.tiles[i+1][j].borders[0]:
                neighbors.append([i + 1, j])

        return neighbors
    
    def solve_DFS(self, instance = None):
        print("Solving Maze with DFS")
        
        # Get the starting point & Goal
        start = [0,0]
        stack = []
        stack.append(start)
        visited = [[False for i in range(self.cols)] for j in range(self.rows)]
        goal = [self.rows - 1, self.cols - 1]
        
        self.__resetColors()

        self.__solve_DFS_Step(stack, visited, goal)
        
    def __solve_DFS_Step(self, stack, visited, goal, instance = None):
            
        if len(stack) == 0:
            print("No Solution")
            return
        
        i,j = stack[-1]
        visited[i][j] = True
        self.tiles[i][j].setColor(self.visitedColor)
        
        self.currentPos = stack[-1]
        self.__renderPlayer()
        
        if stack[-1] == goal:
            print("Goal Reached")
            self.__backTrackPath_DFS(stack)
            return
        
        # Check the left cell
        if j - 1 >= 0 and not visited[i][j - 1]:
            # Left Wall Check
            if not self.tiles[i][j-1].borders[1]:
                # We can go left
                print ("Left")
                stack.append([i, j - 1])
                Clock.schedule_once(partial(self.__solve_DFS_Step,stack, visited, goal), 0.1)
                return
            
        # Check the top cell
        if i - 1 >= 0 and not visited[i - 1][j]:
            # Top Wall Check
            if not self.tiles[i][j].borders[0]:
                # We can go top
                print ("Top")
                stack.append([i - 1, j])
                Clock.schedule_once(partial(self.__solve_DFS_Step,stack,visited, goal), 0.1)
                return
            
            
        # Check the right cell
        if j + 1 < self.cols and not visited[i][j + 1]:
            # Right Wall Check
            if not self.tiles[i][j].borders[1]:
                # We can go right
                print ("Right")
                stack.append([i, j + 1])
                Clock.schedule_once(partial(self.__solve_DFS_Step,stack,visited, goal), 0.1)
                return

        
        # Check the bottom cell
        if i + 1 < self.rows and not visited[i + 1][j]:
            # Bottom Wall Check
            if not self.tiles[i+1][j].borders[0]:
                # We can go bottom
                print ("Bottom")
                stack.append([i + 1, j])
                Clock.schedule_once(partial(self.__solve_DFS_Step,stack,visited, goal), 0.1)
                return
            
        print("BackTracking")
        stack.pop()        
        Clock.schedule_once(partial(self.__solve_DFS_Step,stack, visited, goal), 0.1)

    def __backTrackPath_DFS(self, stack, instance = None):
        if len(stack) == 0:
            return
        i,j = stack[-1]
        self.tiles[i][j].setColor(self.correctPathColor)
        stack.pop()
        Clock.schedule_once(partial(self.__backTrackPath_DFS, stack), 0.1)
        
    def solve_BFS(self, instance = None):
        print("Solving Maze with BFS")
        
        # Get the starting point & Goal
        start = [0,0]
        goal = [self.rows - 1, self.cols - 1]

        deque_BFS = deque()
        deque_BFS.append(start)
        
        visited =[[False for i in range(self.cols)] for j in range(self.rows)]
        parent = [[None for i in range(self.cols)] for j in range(self.rows)]
        
        self.__resetColors()

        self.__solve_BFS_Step(deque_BFS, visited, goal, parent)
        
    def __solve_BFS_Step(self, deque, visited, goal, parent, instance = None):
                        
        if len(deque) == 0:
            print("No Solution")
            return
        
        i,j = deque[0]
        deque.popleft()
        visited[i][j] = True
        self.tiles[i][j].setColor(self.visitedColor)
        
        self.currentPos = [i,j]
        self.__renderPlayer()
        
        if [i,j] == goal:
            print("Reached Goal")
            self.__backTrackPath_BFS(goal, parent)
            return
        
        neighbours = self.__neighbours_unvisited_BFS(i, j, visited)
        
        for neighbour in neighbours:
            deque.append(neighbour)
            parent[neighbour[0]][neighbour[1]] = [i,j]
            
        Clock.schedule_once(partial(self.__solve_BFS_Step,deque, visited, goal, parent), 0.1)
            
    def __backTrackPath_BFS(self, goal, parent, instance = None):
        i,j = goal
        
        if parent[i][j] is None:
            return
        
        self.tiles[i][j].setColor(self.correctPathColor)
        parentI, parentJ = parent[i][j]
        self.tiles[parentI][parentJ].setColor(self.correctPathColor)
        
        Clock.schedule_once(partial(self.__backTrackPath_BFS, [parentI, parentJ], parent), 0.1)
        
        
        
        
        
        
        

        
            



