
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label


Config.set('graphics', 'resizable', True)

class User:
    def __init__(self):
        self.__name = ""
        self.__progress = 0

    def registername(self, newname):
        self.__name = newname
        print(self.__name)
        print("Progress: " + str(self.__progress))

    def updateuserprogress(self, newprog:int):
        self.__progress = newprog

    def getProgress(self):
        return self.__progress

class BisprendEngine(Widget):
    newPlayer = User()
    def checkProgress(self):
        if self.newPlayer.getProgress() == 0:
            name = self.player.text
            self.newPlayer.registername(name)

    def btn(self):
        popup = BisprendPopup()
        self.checkProgress()
        popup.show_popup()


class BisprendPopup(FloatLayout):
    def show_popup(self):
        show = BisprendPopup()
        popupWindow = Popup(title="", content=show,
                            size_hint=(None, None), size=(200, 100))
        popupWindow.open()


class BisprendApp(App):
    def build(self):
        engine = BisprendEngine()
        return engine




#Registering Font
LabelBase.register(name="Mont",
    fn_regular= "Mont-HeavyDEMO.otf"
)

if __name__ == '__main__':
    BisprendApp().run()