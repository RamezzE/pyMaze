class MazeModel:
    def __init__(self, rows, cols):
        
        self.rows = rows
        self.cols = cols
        
        self._currentPos = (0, 0)
        self._startPos = [0, 0]
        self._goalPos = [self.rows - 1, self.cols - 1]
            
    def setPosition(self, pos):
        self.pos = pos
        
    def getPosition(self):
        return self.pos
    
    def setCurrentPos(self, pos):
        self._currentPos = pos
    
    def getCurrentPos(self):
        return self._currentPos
    
    def setGoalPos(self, pos):
        self._goalPos = pos
        
    def getGoalPos(self):
        return self._goalPos
    
    def setStartPos(self, pos):
        self._startPos = pos
        
    def getStartPos(self):
        return self._startPos