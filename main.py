from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.clock import Clock

from maze import Maze

class MazeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.maze = Maze(10, 10, (600,600))
        # maze.setPosition((20,20))
        layout.add_widget(self.maze)
        
        button_generateMaze = Button(text="Generate Maze")
        button_solveDFS = Button(text="Solve with DFS")
        
        button_generateMaze.bind(on_press=self.maze.generateMaze)
        button_solveDFS.bind(on_press=self.maze.solve_DFS)

        layout.add_widget(button_generateMaze)
        layout.add_widget(button_solveDFS)
        return layout

if __name__ == '__main__':
    MazeApp().run()
