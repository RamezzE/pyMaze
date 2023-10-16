from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock

from maze import Maze

class MazeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        maze = Maze(5, 5, (600,600))
        # maze.setPosition((20,20))
        # Clock.schedule_interval(maze.generateMaze, 1)
        maze.generateMaze()
        maze.generateMaze()
        
        # maze.render()
        layout.add_widget(maze)
        
        # Create a button
        button = Button(text="Click Me")
        # button.set_disabled(True)
        # button.size = (20,20)

        # Bind the button's on_release event to the function
        button.bind(on_press=maze.generateMaze)

        layout.add_widget(button)
        
        return layout

if __name__ == '__main__':
    MazeApp().run()
