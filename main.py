from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock
import threading

from maze import Maze

class MazeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.maze = Maze(4, 4, (600,600))
        # maze.setPosition((20,20))
        layout.add_widget(self.maze)
        
        # Create a button
        button = Button(text="Click Me")
        # button.set_disabled(True)
        # button.size = (20,20)

        # Bind the button's on_release event to the function
        button.bind(on_press=self.maze.generateMaze)

        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    MazeApp().run()
