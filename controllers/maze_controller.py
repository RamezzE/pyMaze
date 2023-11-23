import random
from kivy.clock import Clock
from functools import partial
from collections import deque

from tile import Tile

class MazeController:
    def __init__(self, maze):
        self.maze = maze

        self.speed = 0.1
        self.steps = 0

        self.pause = self.isGenerated = False
        
        self.currentAlgorithm = "DFS"

    def __clearMaze(self):
        maze = self.maze
        self.isGenerated = False

        for i in range(1, 6):
            maze.buttons[i].disabled = True

        for i in range(maze.rows):
            for j in range(maze.cols):
                maze.tiles[i][j].setColor(maze.defaultColor)
                maze.tiles[i][j].borderColor = maze.defaultBorderColor
                maze.tiles[i][j].setBorders(0, True)
                maze.tiles[i][j].setBorders(1, True)

    def generateMaze(self, *args):
        maze = self.maze

        self.__clearMaze()

        maze.steps = 0
        maze.stepsLabel.text = f'Steps: {self.steps}'

        # Randomize starting point of maze generation

        i = random.randint(0, maze.rows - 1)
        j = random.randint(0, maze.cols - 1)

        visited = [[False for i in range(maze.cols)] for j in range(maze.rows)]
        stack = [[i, j]]

        maze.buttons[2].disabled = False
        maze.buttons[6].disabled = True

        self.__generateMazeStep(stack, visited)

    def __generateMazeStep(self, stack, visited, *args):

        if (self.pause):
            Clock.schedule_once(
                partial(self.__generateMazeStep, stack, visited), self.speed)
            return

        maze = self.maze

        self.steps += 1
        maze.stepsLabel.text = f'Steps: {self.steps}'

        if len(stack) == 0:
            self.isGenerated = True
            i, j = maze.goalPos
            maze.tiles[i][j].setColor(maze.goalColor)
            maze.currentPos = maze.startPos
            maze._renderPlayer()

            maze.buttons[1].disabled = False
            maze.buttons[4].disabled = False
            maze.buttons[5].disabled = False
            maze.buttons[6].disabled = False

            return

        i, j = stack[-1]

        # Mark the current cell as visited
        visited[i][j] = True

        maze.tiles[i][j].setColor(maze.tileColor)
        maze.tiles[i][j].setBorderColor(maze.borderColor)

        # Update player position on screen
        maze.currentPos = [i, j]
        maze._renderPlayer()

        # Get the unvisited neighbours of the current cell
        neighbours_unvisited = self.__neighbours_unvisited(i, j, visited)

        if len(neighbours_unvisited) == 0:
            stack.pop()
            Clock.schedule_once(
                partial(self.__generateMazeStep, stack, visited), self.speed)
            return

        neighbour = random.choice(neighbours_unvisited)

        # Remove the wall between the current cell and the chosen cell
        nbrI = neighbour[0]
        nbrJ = neighbour[1]

        self.__remove_wall(stack[-1], neighbour)

        stack.append([nbrI, nbrJ])
        Clock.schedule_once(
            partial(self.__generateMazeStep, stack, visited), self.speed)

    def __neighbours_unvisited(self, i, j, visited):
        maze = self.maze
        
        neighbors = []

        # Check the bottom neighbor
        if i + 1 < maze.rows and not visited[i + 1][j]:
            neighbors.append([i + 1, j])

        # Check the top neighbor
        if i - 1 >= 0 and not visited[i - 1][j]:
            neighbors.append([i - 1, j])

        # Check the right neighbor
        if j + 1 < maze.cols and not visited[i][j + 1]:
            neighbors.append([i, j + 1])

        # Check the left neighbor
        if j - 1 >= 0 and not visited[i][j - 1]:
            neighbors.append([i, j - 1])

        return neighbors

    def __neighbours_unvisited_BFS(self, i, j, visited):
        maze = self.maze
        
        neighbors = []

        # Check the left neighbor
        if j - 1 >= 0 and not visited[i][j - 1]:
            if not maze.tiles[i][j-1].borders[1]:
                neighbors.append([i, j - 1])
            
        # Check the top neighbor
        if i - 1 >= 0 and not visited[i - 1][j]:
            if not maze.tiles[i][j].borders[0]:
                neighbors.append([i - 1, j])
            
        # Check the right neighbor
        if j + 1 < maze.cols and not visited[i][j + 1]:
            if not maze.tiles[i][j].borders[1]:
                neighbors.append([i, j + 1])
            
        # Check the bottom neighbor
        if i + 1 < maze.rows and not visited[i + 1][j]:
            if not maze.tiles[i+1][j].borders[0]:
                neighbors.append([i + 1, j])

        return neighbors

    def solveMaze(self, *args):

        if not self.isGenerated:
            return

        maze = self.maze

        maze.buttons[0].disabled = True
        maze.buttons[6].disabled = True

        if self.currentAlgorithm == "DFS":
            self.solve_DFS()
        else:
            self.solve_BFS()

    def solve_DFS(self, *args):

        maze = self.maze

        self.steps = 0
        maze.stepsLabel.text = f'Steps: {self.steps}'

        # Create a stack for DFS
        stack = []
        stack.append(maze.startPos)

        # Create a visited array
        visited = [[False for i in range(maze.cols)] for j in range(maze.rows)]

        maze._resetColors()

        self.__solve_DFS_Step(stack, visited, maze.goalPos)

    def __solve_DFS_Step(self, stack, visited, goal, *args):

        if (self.pause):
            Clock.schedule_once(
                partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
            return

        maze = self.maze

        self.steps += 1
        maze.stepsLabel.text = f'Steps: {self.steps}'

        if len(stack) == 0:
            print("No Solution")
            return

        i, j = stack[-1]
        visited[i][j] = True
        maze.tiles[i][j].setColor(maze.visitedColor)

        maze.currentPos = stack[-1]
        maze._renderPlayer()

        if stack[-1] == goal:
            # Reached Goal
            self.__backTrackPath_DFS(stack)
            return

        # Check the left cell
        if j - 1 >= 0 and not visited[i][j - 1]:
            # Left Wall Check
            if not maze.tiles[i][j-1].borders[1]:
                # We can go left
                stack.append([i, j - 1])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # Check the top cell
        if i - 1 >= 0 and not visited[i - 1][j]:
            # Top Wall Check
            if not maze.tiles[i][j].borders[0]:
                # We can go top
                stack.append([i - 1, j])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # Check the right cell
        if j + 1 < maze.cols and not visited[i][j + 1]:
            # Right Wall Check
            if not maze.tiles[i][j].borders[1]:
                # We can go right
                stack.append([i, j + 1])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # Check the bottom cell
        if i + 1 < maze.rows and not visited[i + 1][j]:
            # Bottom Wall Check
            if not maze.tiles[i+1][j].borders[0]:
                # We can go bottom
                stack.append([i + 1, j])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # No Unvisited Neighbours found, go back (Backtracking)
        stack.pop()
        Clock.schedule_once(partial(self.__solve_DFS_Step,
                            stack, visited, goal), self.speed)

    def solve_BFS(self, instance=None):

        maze = self.maze

        self.steps = 0
        maze.stepsLabel.text = f'Steps: {self.steps}'

        # Create a queue for BFS
        deque_BFS = deque()
        deque_BFS.append(maze.startPos)

        # Creating a visited array
        visited = [[False for i in range(maze.cols)] for j in range(maze.rows)]

        # Creating a parent array to track correct path
        parent = [[None for i in range(maze.cols)] for j in range(maze.rows)]

        maze._resetColors()

        self.__solve_BFS_Step(deque_BFS, visited, maze.goalPos, parent)

    def __solve_BFS_Step(self, deque, visited, goal, parent, *args):

        if (self.pause):
            Clock.schedule_once(
                partial(self.__solve_BFS_Step, deque, visited, goal, parent), self.speed)
            return

        maze = self.maze

        self.steps += 1
        maze.stepsLabel.text = f'Steps: {self.steps}'

        if len(deque) == 0:
            print("No Solution")
            return

        i, j = deque[0]
        deque.popleft()
        visited[i][j] = True
        maze.tiles[i][j].setColor(maze.visitedColor)

        maze.currentPos = [i, j]
        maze._renderPlayer()

        if [i, j] == goal:
            # Reached Goal
            self.__backTrackPath_BFS(goal, parent)
            return

        neighbours = self.__neighbours_unvisited_BFS(i, j, visited)

        for neighbour in neighbours:
            deque.append(neighbour)
            parent[neighbour[0]][neighbour[1]] = [i, j]

        Clock.schedule_once(partial(self.__solve_BFS_Step,
                            deque, visited, goal, parent), self.speed)

    def __backTrackPath_DFS(self, stack, *args):

        maze = self.maze

        if len(stack) == 0:
            maze.buttons[0].disabled = False
            maze.buttons[4].disabled = False
            maze.buttons[5].disabled = False
            maze.buttons[6].disabled = False
            return

        i, j = stack[-1]
        maze.tiles[i][j].setColor(maze.correctPathColor)
        stack.pop()
        Clock.schedule_once(
            partial(self.__backTrackPath_DFS, stack), self.speed)

    def __backTrackPath_BFS(self, goal, parent, *args):
        i, j = goal
        
        maze = self.maze

        if parent[i][j] is None:
            maze.buttons[0].disabled = False
            maze.buttons[4].disabled = False
            maze.buttons[5].disabled = False
            maze.buttons[6].disabled = False
            return

        maze.tiles[i][j].setColor(maze.correctPathColor)
        parentI, parentJ = parent[i][j]
        maze.tiles[parentI][parentJ].setColor(maze.correctPathColor)

        Clock.schedule_once(partial(self.__backTrackPath_BFS, [
                            parentI, parentJ], parent), self.speed)
        
    def togglePause(self, *args):
        self.pause = not self.pause
        
        maze = self.maze
        
        if self.pause:
            maze.buttons[2].disabled = True
            maze.buttons[3].disabled = False
        else:
            maze.buttons[3].disabled = True
            maze.buttons[2].disabled = False
        
    def toggleChangeMazeStart(self, button):
        maze = self.maze
        
        maze.chooseStart = True
        maze.chooseEnd = False
        
        for i in range(4,7):
            maze.buttons[i].disabled = True
        
    def toggleChangeMazeEnd(self, button):
        maze = self.maze
        
        maze.chooseStart = False
        maze.chooseEnd = True
        
        for i in range(4,7):
            maze.buttons[i].disabled = True   
        
    @staticmethod    
    def changeGoal(maze, newGoal):   
        
        maze.goalPos = newGoal    
        maze._resetColors()
        for i in range(4,7):
            maze.buttons[i].disabled = False
            
    @staticmethod
    def changeStart(maze, newStart):
        
        maze.startPos = newStart
        maze.currentPos = newStart
        maze.startPos = newStart
        
        maze._resetColors()
        maze._renderPlayer()
        for i in range(4,7):
            maze.buttons[i].disabled = False
            
    def changeAlgorithm(self, algorithm, *args):
        self.currentAlgorithm = algorithm 
        
    def __remove_wall(self, currentCell, neighbour):
        
        maze = self.maze
        
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
                
        maze.tiles[i][j].setBorders(wall, False)
        
    @staticmethod
    def update_rows_cols(maze, rows, cols, *args):
        maze.clear_widgets()
        
        maze.rows = rows
        maze.cols = cols
        
        maze.currentPos = [0,0]
        maze.goalPos = [rows-1, cols-1]
        
        maze.tiles = [[None for j in range(maze.cols)] for i in range(maze.rows)]
        
        for i in range(maze.rows):
            for j in range(maze.cols):
                maze.tiles[i][j] = Tile()
                maze.add_widget(maze.tiles[i][j])
                
        try:
            for i in range(1,6):
                maze.buttons[i].disabled = True
        except:
            pass
        
        maze._render()