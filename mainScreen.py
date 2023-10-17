from kivy.uix.widget import Widget
from maze import Maze
from kivy.uix.button import Button  
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from functools import partial
from kivy.graphics.context_instructions import Color

class MainScreen(Widget):
    def __init__(self, **kwargs):
        
        self.Maze = Maze(10,10)
        self.Maze.resize(self.size)
        self.currentAlgorithm = "DFS"
        
        self.textColor = (231/255, 157/255, 86/255,1)
        self.buttonBackgroundColor = (40/255, 90/255, 107/255,1)
                
        self.__initButtons()
        
        self.root = BoxLayout(orientation='horizontal')
        self.root.add_widget(self.Maze)
        self.root.add_widget(self.buttonsBox)
        
        Window.clearcolor = (0.3, 0.3, 0.3, 1)
        
    def __initButtons(self):
        self.buttons = []
        for i in range(2):
            self.buttons.append(Button())
        
        self.buttons[0].text = "Generate Maze"
        self.buttons[1].text = "Solve Maze"
        
        self.buttons[0].bind(on_release=self.Maze.generateMaze)
        self.buttons[1].bind(on_release=self.Maze.solveMaze)
        
        self.buttonsBox = BoxLayout(orientation='vertical')
        self.buttonsBox.size_hint_max = (Window.width/4, Window.height/4)
        self.buttonsBox.padding = 10
                
        self.stepsLabel =  Label(text=f'Steps: {self.Maze.steps}')
        self.stepsLabel.color = self.textColor
        
        self.buttonsBox.add_widget(self.stepsLabel)
        
        self.Maze.initLabels(self.stepsLabel)
        
        for button in self.buttons:
            self.buttonsBox.add_widget(button)
            button.size_hint_max = (button.parent.width, button.parent.height/2)
            button.margin = 10
            button.color = self.textColor
            button.background_color = self.buttonBackgroundColor

        self.__initRadioButtons()
        self.buttonsBox.add_widget(self.radioButtonsBox)
        
        self.buttonsBox.canvas.add(Color(rgba=self.textColor))
            
    def __initRadioButtons(self):
        self.radioButtons = []
        self.radioLabels = []

        for i in range(2):
            self.radioButtons.append(CheckBox(group = "solveMaze_group"))
            self.radioLabels.append(Label())
        
        self.radioLabels[0].text = "DFS"
        self.radioLabels[1].text = "BFS"

        self.radioButtons[0].bind(active=partial(self.Maze.changeAlgorithm, "DFS"))
        self.radioButtons[1].bind(active=partial(self.Maze.changeAlgorithm, "BFS"))

        self.radioButtons[0].active = True
        self.radioButtons[1].active = False
        
        self.radioButtonsBox = BoxLayout(orientation='horizontal')
        self.radioButtonsBox.size_hint_max = (Window.width/4, Window.height/4)
        self.radioButtonsBox.padding = 10
        
        for button in self.radioButtons:
            # self.radioButtonsBox.add_widget(button)
            # button.size_hint_max = (button.parent.width, button.parent.height/2)
            button.margin = 10
            
        for label in self.radioLabels:
            label.color = self.textColor
            # label.size_hint_max = (label.parent.width, label.parent.height/2)
            # label.margin = 10
            
        self.radioButtonsBox.add_widget(self.radioLabels[0])
        self.radioButtonsBox.add_widget(self.radioButtons[0])
        self.radioButtonsBox.add_widget(self.radioLabels[1])
        self.radioButtonsBox.add_widget(self.radioButtons[1])
        
    def getRoot(self):
        return self.root
        

