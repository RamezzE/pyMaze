from kivy.uix.widget import Widget
from kivy.uix.button import Button  
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from functools import partial
from kivy.uix.slider import Slider
from kivy.graphics.context_instructions import Color

from controllers.maze_controller import MazeController

class MainScreen(Widget):
    def __init__(self, **kwargs):
        self.buttons = []
        self.rows = 5
        self.cols = 5
        
        self.mazeController = MazeController(self.rows,self.cols)
        self.mazeController.linkButtons(self.buttons)
        
        # self.textColor = (231/255, 157/255, 86/255,1)
        self.textColor = (1,1,1,1)
        self.buttonBackgroundColor = (40/255, 90/255, 107/255,1)
        
        self.__initButtons()
        
        self.root = BoxLayout(orientation='horizontal')
        self.root.add_widget(self.mazeController.getView())
        self.root.add_widget(self.buttonsBox)
        
        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        
    def __initSliders(self):
        self.sliders = []
        for i in range(2):
            self.sliders.append(Slider(min = 1, max = 40, step = 1))    
            self.sliders[i].bind(value=lambda instance, value, i=i: self.__on_slider_value(instance, value, i))
        
        self.sliders[0].value = self.rows
        self.sliders[1].value = self.cols
        
        self.sliderLabels = []
        for i in range (len(self.sliders)):
            self.sliderLabels.append(Label())
            
        self.sliderLabels[0].text = "Rows: " + str(self.rows)
        self.sliderLabels[1].text = "Cols: " + str(self.cols)
        
        self.slidersBox = BoxLayout(orientation = "vertical")
        
        hbox = BoxLayout(orientation = "horizontal")
        
        hbox.add_widget(self.sliderLabels[0])
        hbox.add_widget(self.sliders[0])
        
        self.slidersBox.add_widget(hbox)
        
        hbox = BoxLayout(orientation = "horizontal")
        
        hbox.add_widget(self.sliderLabels[1])
        hbox.add_widget(self.sliders[1])
        
        self.slidersBox.add_widget(hbox)
          
    def __on_slider_value(self, instance, value, i):
        try:
            if i == 0:
                self.sliderLabels[i].text = f"Rows: {int(value)}"
            elif i == 1:
                self.sliderLabels[i].text = f"Cols: {int(value)}"
            else:
                self.sliderLabels[i].text = f"Speed: {float(value)}x"
                self.mazeController.speed = float(1/(value*10))
        except:
            pass

    def __initButtons(self):
        for i in range(7):
            self.buttons.append(Button())
        
        self.buttons[0].text = "Generate Maze"
        self.buttons[1].text = "Solve Maze"
        self.buttons[2].text = "Pause"
        self.buttons[3].text = "Continue"
        self.buttons[4].text = "Choose Start"
        self.buttons[5].text = "Choose End"
        self.buttons[6].text = "Apply"
        
        for i in range(1,6):
            self.buttons[i].disabled = True
        
        self.buttons[0].bind(on_release=self.mazeController.generateMaze)
        self.buttons[1].bind(on_release=self.mazeController.solveMaze)
        
        self.buttons[4].bind(on_release=self.mazeController.toggleChangeMazeStart)  
        self.buttons[5].bind(on_release=self.mazeController.toggleChangeMazeEnd)  
        
        self.buttonsBox = BoxLayout(orientation='vertical',padding = 10, spacing = 2)
        
        stepsLabel =  Label()
        stepsLabel.color = self.textColor
        
        self.buttonsBox.add_widget(stepsLabel)
        
        self.mazeController.mazeView.initLabels(stepsLabel)
        
        for i in range(2):
            self.buttonsBox.add_widget(self.buttons[i])
            self.buttons[i].size_hint_max = (self.buttons[i].parent.width, self.buttons[i].parent.height/2)
            
        pause_continue_button_box = BoxLayout(orientation = "horizontal", spacing = self.buttonsBox.spacing)
        
        for i in range(2,4):
            pause_continue_button_box.add_widget(self.buttons[i])
            self.buttons[i].size_hint_y = None
            self.buttons[i].height = self.buttons[i-2].height
            self.buttons[i].bind(on_release = self.mazeController.togglePause)
            
        for i in range(4,6):
            self.buttons[i].size_hint_y = None
            self.buttons[i].height = self.buttons[i-2].height
        
        for button in self.buttons:
            button.color = self.textColor
            button.background_color = self.buttonBackgroundColor
            
        self.__initSliders()
        
        speedHbox = BoxLayout(orientation = "horizontal")
        self.sliderLabels.append(Label(text = "Speed: 1.0x"))
        speedHbox.add_widget(self.sliderLabels[2])
        
        self.sliders.append(Slider(min = 1, max = 10, value = 1, step = 0.5))
        self.sliders[2].bind(value=lambda instance, value, i=2: self.__on_slider_value(instance, value, i))

        speedHbox.add_widget(self.sliders[2])
            
        hbox = BoxLayout(orientation = "horizontal")

        hbox.add_widget(self.buttons[4])
        hbox.add_widget(self.buttons[5])

        self.__initRadioButtons()
        self.buttonsBox.add_widget(self.radioButtonsBox)    
        self.buttonsBox.add_widget(pause_continue_button_box)
        self.buttonsBox.add_widget(speedHbox)
        self.buttonsBox.add_widget(hbox)
        
        self.buttons[6].bind(on_release=lambda button: MazeController.update_rows_cols(self.mazeController.mazeView,int(self.sliders[0].value), int(self.sliders[1].value)))

        self.slidersBox.add_widget(self.buttons[6])
        self.buttonsBox.add_widget(self.slidersBox)
        
        self.buttonsBox.canvas.add(Color(rgba=self.textColor))
              
    def __initRadioButtons(self):
        self.radioButtons = []
        self.radioLabels = []

        for i in range(2):
            self.radioButtons.append(CheckBox(group = "solveMaze_group"))
            self.radioLabels.append(Label())
        
        self.radioLabels[0].text = "DFS"
        self.radioLabels[1].text = "BFS"

        self.radioButtons[0].bind(active=partial(self.mazeController.changeAlgorithm, "DFS"))
        self.radioButtons[1].bind(active=partial(self.mazeController.changeAlgorithm, "BFS"))

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