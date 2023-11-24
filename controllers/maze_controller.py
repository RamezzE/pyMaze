import random
from kivy.core.window import Window
from kivy.clock import Clock
from functools import partial
from collections import deque

from controllers.tile_controller import TileController
from models.maze_model import MazeModel
from views.maze_view import MazeView

class MazeController:
    def __init__(self, rows, cols):
        

        self.pause = self.isGenerated = self.chooseStart = self.chooseEnd = False
        self.currentAlgorithm = "DFS"

        self.speed = 0.1
        self.steps = 0
        
        self.mazeModel = MazeModel(rows=rows, cols=cols)
        self.tileController = TileController(self)
        self.mazeView = MazeView(self.mazeModel, self.tileController.on_touch_down)

        self.mazeView.resize((Window.height, Window.height))
        Window.bind(on_resize=lambda window, width,
                    height: self.mazeView.resize((height, height)))

    def __clearMaze(self):
        self.isGenerated = False
        self.mazeView.clearMaze()

    def generateMaze(self, *args):

        self.__clearMaze()

        self.__resetSteps()

        # Randomize starting point of mazeView generation
        i = random.randint(0, self.mazeModel.rows - 1)
        j = random.randint(0, self.mazeModel.cols - 1)

        visited = [[False for i in range(self.mazeModel.cols)]
                   for j in range(self.mazeModel.rows)]
        stack = [[i, j]]

        self.mazeView.enableButtons([2,6])
        
        self.__generateMazeStep(stack, visited)

    def __generateMazeStep(self, stack, visited, *args):

        if (self.pause):
            Clock.schedule_once(
                partial(self.__generateMazeStep, stack, visited), self.speed)
            return

        self.__incrementSteps()

        if len(stack) == 0:
            self.isGenerated = True

            self.mazeView.colorGoal()

            self.mazeModel.setCurrentPos(self.mazeModel.getStartPos())
            self.mazeView.renderPlayer()

            self.mazeView.enableButtons([1, 4, 5, 6])
            return

        i, j = stack[-1]

        # Mark the current cell as visited
        visited[i][j] = True

        self.mazeView.colorTile(i, j)
        self.mazeView.colorBorder(i, j)

        # Update player position on screen
        self.mazeModel.setCurrentPos([i, j])
        self.mazeView.renderPlayer()

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
        neighbors = []

        # Check the bottom neighbor
        if i + 1 < self.mazeModel.rows and not visited[i + 1][j]:
            neighbors.append([i + 1, j])

        # Check the top neighbor
        if i - 1 >= 0 and not visited[i - 1][j]:
            neighbors.append([i - 1, j])

        # Check the right neighbor
        if j + 1 < self.mazeModel.cols and not visited[i][j + 1]:
            neighbors.append([i, j + 1])

        # Check the left neighbor
        if j - 1 >= 0 and not visited[i][j - 1]:
            neighbors.append([i, j - 1])

        return neighbors

    def __neighbours_unvisited_BFS(self, i, j, visited):
        neighbors = []

        # Check the left neighbor
        if j - 1 >= 0 and not visited[i][j - 1]:
            if not self.mazeView.getBorder(i, j-1, 1):
                neighbors.append([i, j - 1])

        # Check the top neighbor
        if i - 1 >= 0 and not visited[i - 1][j]:
            if not self.mazeView.getBorder(i, j, 0):
                neighbors.append([i - 1, j])

        # Check the right neighbor
        if j + 1 < self.mazeModel.cols and not visited[i][j + 1]:
            if not self.mazeView.getBorder(i, j, 1):
                neighbors.append([i, j + 1])

        # Check the bottom neighbor
        if i + 1 < self.mazeModel.rows and not visited[i + 1][j]:
            if not self.mazeView.getBorder(i+1, j, 0):
                neighbors.append([i + 1, j])

        return neighbors

    def solveMaze(self, *args):

        if not self.isGenerated:
            return

        self.mazeView.disableButtons([0, 6])

        if self.currentAlgorithm == "DFS":
            self.solve_DFS()
        else:
            self.solve_BFS()

    def solve_DFS(self, *args):

        self.__resetSteps()

        # Create a stack for DFS
        stack = []
        stack.append(self.mazeModel.getStartPos())

        # Create a visited array
        visited = [[False for i in range(self.mazeModel.cols)]
                   for j in range(self.mazeModel.rows)]

        self.mazeView._resetColors()

        self.__solve_DFS_Step(stack, visited, self.mazeModel.getGoalPos())

    def __solve_DFS_Step(self, stack, visited, goal, *args):

        if (self.pause):
            Clock.schedule_once(
                partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
            return

        self.__incrementSteps()

        if len(stack) == 0:
            print("No Solution")
            return

        i, j = stack[-1]
        visited[i][j] = True

        self.mazeView.markAsVisited(i, j)
        self.mazeModel.setCurrentPos(stack[-1])
        self.mazeView.renderPlayer()

        if stack[-1] == goal:
            # Reached Goal
            self.__backTrackPath_DFS(stack)
            return

        # Check the left cell
        if j - 1 >= 0 and not visited[i][j - 1]:
            # Left Wall Check
            if not self.mazeView.getBorder(i, j-1, 1):
                # We can go left
                stack.append([i, j - 1])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # Check the top cell
        if i - 1 >= 0 and not visited[i - 1][j]:
            # Top Wall Check
            if not self.mazeView.getBorder(i, j, 0):
                # We can go top
                stack.append([i - 1, j])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # Check the right cell
        if j + 1 < self.mazeModel.cols and not visited[i][j + 1]:
            # Right Wall Check
            if not self.mazeView.getBorder(i, j, 1):
                # We can go right
                stack.append([i, j + 1])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # Check the bottom cell
        if i + 1 < self.mazeModel.rows and not visited[i + 1][j]:
            # Bottom Wall Check
            if not self.mazeView.getBorder(i+1, j, 0):
                # We can go bottom
                stack.append([i + 1, j])
                Clock.schedule_once(
                    partial(self.__solve_DFS_Step, stack, visited, goal), self.speed)
                return

        # No Unvisited Neighbours found, go back (Backtracking)
        stack.pop()
        Clock.schedule_once(partial(self.__solve_DFS_Step,
                            stack, visited, goal), self.speed)

    def solve_BFS(self, *args):

        self.__resetSteps()

        # Create a queue for BFS
        deque_BFS = deque()
        deque_BFS.append(self.mazeModel.getStartPos())

        # Creating a visited array
        visited = [[False for i in range(self.mazeModel.cols)]
                   for j in range(self.mazeModel.rows)]

        # Creating a parent array to track correct path
        parent = [[None for i in range(self.mazeModel.cols)]
                  for j in range(self.mazeModel.rows)]

        self.mazeView._resetColors()

        self.__solve_BFS_Step(deque_BFS, visited,
                              self.mazeModel.getGoalPos(), parent)

    def __solve_BFS_Step(self, deque, visited, goal, parent, *args):

        if (self.pause):
            Clock.schedule_once(
                partial(self.__solve_BFS_Step, deque, visited, goal, parent), self.speed)
            return

        self.__incrementSteps()

        if len(deque) == 0:
            print("No Solution")
            return

        i, j = deque[0]
        deque.popleft()
        visited[i][j] = True
        self.mazeView.markAsVisited(i,j)

        self.mazeModel.setCurrentPos([i, j])
        self.mazeView.renderPlayer()

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

        if len(stack) == 0:
            self.mazeView.enableButtons([0, 4, 5, 6])
            return

        i, j = stack[-1]
        self.mazeView.markAsCorrectPath(i,j)
        stack.pop()
        Clock.schedule_once(
            partial(self.__backTrackPath_DFS, stack), self.speed)

    def __backTrackPath_BFS(self, goal, parent, *args):
        i, j = goal

        if parent[i][j] is None:
            self.mazeView.enableButtons([0, 4, 5, 6])
            return

        self.mazeView.markAsCorrectPath(i,j)
        parentI, parentJ = parent[i][j]
        self.mazeView.markAsCorrectPath(parentI, parentJ)

        Clock.schedule_once(partial(self.__backTrackPath_BFS, [
                            parentI, parentJ], parent), self.speed)

    def togglePause(self, *args):
        self.pause = not self.pause

        if self.pause:
            self.mazeView.disableButtons[[2]]
            self.mazeView.enableButtons([3])
        else:
            self.mazeView.disableButtons[[3]]
            self.mazeView.enableButtons([2])

    def toggleChangeMazeStart(self, *args):
        self.chooseStart = True
        self.chooseEnd = False

        self.mazeView.disableButtons([4, 5,6])

    def toggleChangeMazeEnd(self, *args):
        self.chooseStart = False
        self.chooseEnd = True

        self.mazeView.disableButtons([4, 5,6])

    def changeGoal(self, newGoal):
        print("change goal")
        self.chooseEnd = False
        self.mazeView.mazeModel.setGoalPos(newGoal)
        self.mazeView._resetColors()
        
        self.mazeView.enableButtons([4, 5, 6])

    def changeStart(self,newStart):

        self.chooseStart = False
        self.mazeView.mazeModel.setStartPos(newStart)
        self.mazeView.mazeModel.setCurrentPos(newStart)
        self.mazeView.mazeModel.setStartPos(newStart)

        self.mazeView._resetColors()
        self.mazeView.renderPlayer()
        self.mazeView.enableButtons([4, 5,6])

    def changeAlgorithm(self, algorithm, *args):
        self.currentAlgorithm = algorithm

    def __remove_wall(self, currentCell, neighbour):

        # Same row
        if currentCell[0] == neighbour[0]:
            wall = 1  # Right or Left Wall to be removed
            i = currentCell[0] = neighbour[0]
            if currentCell[1] > neighbour[1]:
                # Left Wall which is -> Right Wall of Neighbour to be removed
                j = neighbour[1]
            else:
                # Right Wall of currentCell to be removed
                j = currentCell[1]

        # Same Column
        else:
            wall = 0  # Top or Bottom Wall to be removed
            j = currentCell[1] = neighbour[1]
            if currentCell[0] < neighbour[0]:
                # Bottom Wall which is -> Top Wall of Neighbour to be removed
                i = neighbour[0]
            else:
                # Top Wall of CurrentCell to be removed
                i = currentCell[0]

        self.mazeView.setBorder(i, j, wall, False)

    @staticmethod
    def update_rows_cols(mazeView, rows, cols, *args):

        mazeView.mazeModel.rows = rows
        mazeView.mazeModel.cols = cols

        mazeView.mazeModel.setCurrentPos([0, 0])
        mazeView.mazeModel.setStartPos([0, 0])
        mazeView.mazeModel.setGoalPos([rows-1, cols-1])
        
        mazeView.resetMaze()

    def linkButtons(self, buttons):
        self.mazeView._buttons = buttons
        
    def __incrementSteps(self):
        self.steps += 1
        self.mazeView.updateStepsLabel(f'Steps: {self.steps}')
        
    def __resetSteps(self):
        self.steps = 0
        self.mazeView.updateStepsLabel(f'Steps: {self.steps}')
        
    def getView(self):
        return self.mazeView
