import kivy

from kivy.app import App
from kivy.uix.widget import Widget

class BisprendEngine(Widget):
    pass

class BisprendApp(App):
    def build(self):
        return BisprendEngine()

class User:
    def __init__(self):
        self.__name = ""
        self.__progress = 0

    def registername(self, newname):
        self.__name = newname

    def updateuserprogress(self, newprog:int):
        self.__progress = newprog

if __name__ == '__main__':
    BisprendApp().run()