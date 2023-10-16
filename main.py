from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from maze import Maze

class MazeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        maze = Maze(10, 10, (Window.width/1.5, Window.width/1.5 ))
        layout.add_widget(maze)
        return layout

if __name__ == '__main__':
    MazeApp().run()
