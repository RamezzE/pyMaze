from kivy.app import App
from views.mainScreen_view import MainScreen

class MazeApp(App):
    def build(self):
        screen = MainScreen()
        return screen.getRoot()

if __name__ == '__main__':
    MazeApp().run()