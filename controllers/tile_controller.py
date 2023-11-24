class TileController:
    def __init__(self, mazeController):
        self.mazeController = mazeController
    
    def on_touch_down(self, tile, touch):
        if self.mazeController.chooseEnd == True:
            if tile.collide_point(*touch.pos):   
                self.mazeController.changeGoal(tile.getIndex())
                
        elif self.mazeController.chooseStart == True:
            if tile.collide_point(*touch.pos):
                self.mazeController.changeStart(tile.getIndex())

    