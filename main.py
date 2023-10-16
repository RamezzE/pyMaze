from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button

from maze import Maze

class MazeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        maze = Maze(10, 10, (Window.width/1.5, Window.width/1.5 ))
        maze.setPosition((20,20))
        maze.generateMaze()
        
        # maze.render()
        layout.add_widget(maze)
        
        # Create a button
        # button = Button(text="Click Me")
        # button.set_disabled(True)
        # button.size_hint_max = (100,100)

        # Bind the button's on_release event to the function
        # button.bind(on_release=maze.generateMaze)

        # layout.add_widget(button)
        
        return layout

if __name__ == '__main__':
    MazeApp().run()
